import json
import uuid
import hashlib
import os
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool


# ── Engine selection ────────────────────────────────────────────────────────
# If a DATABASE_URL is configured (Streamlit secret or environment variable),
# the app uses that persistent database (e.g. Supabase Postgres). Otherwise it
# falls back to a local SQLite file for development.

def _database_url():
    url = None
    try:
        import streamlit as st
        if "DATABASE_URL" in st.secrets:
            url = st.secrets["DATABASE_URL"]
    except Exception:
        pass
    if not url:
        url = os.environ.get("DATABASE_URL")
    return url


def _make_engine():
    url = _database_url()
    if url:
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return create_engine(
            url,
            poolclass=NullPool,           # safe with Supabase transaction pooler
            connect_args={"sslmode": "require"},
        )
    return create_engine("sqlite:///music_rec.db")


_engine = _make_engine()
_IS_PG = _engine.dialect.name == "postgresql"


def _exec(sql, params=None):
    with _engine.begin() as conn:
        conn.execute(text(sql), params or {})


def _query(sql, params=None):
    with _engine.connect() as conn:
        rows = conn.execute(text(sql), params or {}).mappings().all()
    return [dict(r) for r in rows]


def _migrate_sqlite_column(table, column, decl):
    """Add a missing column to an existing SQLite table (local dev only)."""
    cols = [c["name"] for c in _query(f"PRAGMA table_info({table})")]
    if column not in cols:
        _exec(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


# ── Sessions ────────────────────────────────────────────────────────────────

def init_db():
    _exec("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            mode TEXT,
            seed_artists TEXT,
            recommendations TEXT,
            rating_relevance INTEGER,
            rating_mode_fit INTEGER,
            rating_explanation INTEGER,
            comment TEXT,
            timestamp TEXT,
            user_id TEXT
        )
    """)
    if not _IS_PG:
        _migrate_sqlite_column("sessions", "user_id", "TEXT")


def new_session_id():
    return str(uuid.uuid4())


def save_session(session_id, mode, seed_artists, recommendations,
                 rating_relevance, rating_mode_fit, rating_explanation, comment,
                 user_id=None):
    rec_names = [f"{r['name']} - {r['artist']}" for r in recommendations]
    params = {
        "session_id": session_id, "mode": mode,
        "seed_artists": json.dumps(seed_artists),
        "recommendations": json.dumps(rec_names),
        "rating_relevance": rating_relevance,
        "rating_mode_fit": rating_mode_fit,
        "rating_explanation": rating_explanation,
        "comment": comment, "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
    }
    cols = ("session_id, mode, seed_artists, recommendations, rating_relevance, "
            "rating_mode_fit, rating_explanation, comment, timestamp, user_id")
    vals = (":session_id, :mode, :seed_artists, :recommendations, :rating_relevance, "
            ":rating_mode_fit, :rating_explanation, :comment, :timestamp, :user_id")
    if _IS_PG:
        sql = f"""
            INSERT INTO sessions ({cols}) VALUES ({vals})
            ON CONFLICT (session_id) DO UPDATE SET
                mode = EXCLUDED.mode,
                seed_artists = EXCLUDED.seed_artists,
                recommendations = EXCLUDED.recommendations,
                rating_relevance = EXCLUDED.rating_relevance,
                rating_mode_fit = EXCLUDED.rating_mode_fit,
                rating_explanation = EXCLUDED.rating_explanation,
                comment = EXCLUDED.comment,
                timestamp = EXCLUDED.timestamp,
                user_id = EXCLUDED.user_id
        """
    else:
        sql = f"INSERT OR REPLACE INTO sessions ({cols}) VALUES ({vals})"
    _exec(sql, params)


def get_all_sessions():
    return _query("SELECT * FROM sessions")


# ── Per-track feedback ──────────────────────────────────────────────────────

def init_track_feedback():
    id_decl = "SERIAL PRIMARY KEY" if _IS_PG else "INTEGER PRIMARY KEY AUTOINCREMENT"
    _exec(f"""
        CREATE TABLE IF NOT EXISTS track_feedback (
            id {id_decl},
            session_id TEXT,
            mode TEXT,
            track_name TEXT,
            artist TEXT,
            feedback TEXT,
            timestamp TEXT,
            user_id TEXT
        )
    """)
    if not _IS_PG:
        _migrate_sqlite_column("track_feedback", "user_id", "TEXT")


def save_track_feedback(session_id, mode, track_name, artist, feedback, user_id=None):
    _exec("""
        INSERT INTO track_feedback
            (session_id, mode, track_name, artist, feedback, timestamp, user_id)
        VALUES (:session_id, :mode, :track_name, :artist, :feedback, :timestamp, :user_id)
    """, {
        "session_id": session_id, "mode": mode, "track_name": track_name,
        "artist": artist, "feedback": feedback,
        "timestamp": datetime.now().isoformat(), "user_id": user_id,
    })


def get_all_track_feedback():
    return _query("SELECT * FROM track_feedback")


# ── Accounts (optional sign-in) ─────────────────────────────────────────────

def init_users():
    _exec("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT,
            created_at TEXT
        )
    """)


def _hash_password(password, salt):
    """Salted PBKDF2-HMAC-SHA256 hash (standard-library only, no plaintext stored)."""
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()


def create_user(username, password):
    """Create an account. Returns (True, user_id) or (False, error_message)."""
    username = (username or "").strip()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password or "") < 4:
        return False, "Password must be at least 4 characters."

    exists = _query(
        "SELECT 1 AS one FROM users WHERE LOWER(username) = LOWER(:u)",
        {"u": username},
    )
    if exists:
        return False, "That username is already taken."

    user_id = str(uuid.uuid4())
    salt = os.urandom(16).hex()
    pw_hash = _hash_password(password, salt)
    _exec(
        "INSERT INTO users (user_id, username, password_hash, salt, created_at) "
        "VALUES (:user_id, :username, :pw, :salt, :created)",
        {"user_id": user_id, "username": username, "pw": pw_hash,
         "salt": salt, "created": datetime.now().isoformat()},
    )
    return True, user_id


def authenticate(username, password):
    """Return user_id on success, or None on failure."""
    username = (username or "").strip()
    rows = _query(
        "SELECT user_id, password_hash, salt FROM users "
        "WHERE LOWER(username) = LOWER(:u)", {"u": username},
    )
    if not rows:
        return None
    row = rows[0]
    if _hash_password(password, row["salt"]) == row["password_hash"]:
        return row["user_id"]
    return None


def get_username(user_id):
    rows = _query("SELECT username FROM users WHERE user_id = :uid", {"uid": user_id})
    return rows[0]["username"] if rows else None


def get_user_liked_artists(user_id, limit=20):
    """Artists a signed-in user has liked before, most-liked first."""
    if not user_id:
        return []
    rows = _query(
        "SELECT artist, COUNT(*) AS c FROM track_feedback "
        "WHERE user_id = :uid AND LOWER(feedback) = 'like' AND artist IS NOT NULL "
        "GROUP BY artist ORDER BY c DESC LIMIT :lim",
        {"uid": user_id, "lim": limit},
    )
    return [r["artist"] for r in rows]


if __name__ == "__main__":
    init_db()
    init_track_feedback()
    init_users()
    print("Database initialised. Backend:", "Postgres" if _IS_PG else "SQLite")
    sid = new_session_id()
    save_session(sid, "Focus", ["Radiohead"], [{"name": "Test", "artist": "X"}],
                 5, 4, 5, "good")
    print("Saved test session:", sid)
    print("Total sessions:", len(get_all_sessions()))
