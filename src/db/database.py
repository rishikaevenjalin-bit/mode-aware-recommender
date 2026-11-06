import sqlite3
import json
import uuid
import hashlib
import os
from datetime import datetime

DB_PATH = "music_rec.db"


# ── Schema helpers ──────────────────────────────────────────────────────────

def _ensure_column(conn, table, column, decl):
    """Add a column to an existing table if it isn't already there."""
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
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
    _ensure_column(conn, "sessions", "user_id", "TEXT")  # migrate old databases
    conn.commit()
    conn.close()

def new_session_id():
    return str(uuid.uuid4())

def save_session(session_id, mode, seed_artists, recommendations,
                 rating_relevance, rating_mode_fit, rating_explanation, comment,
                 user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rec_names = [f"{r['name']} - {r['artist']}" for r in recommendations]
    c.execute("""
        INSERT OR REPLACE INTO sessions
        (session_id, mode, seed_artists, recommendations,
         rating_relevance, rating_mode_fit, rating_explanation, comment,
         timestamp, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id, mode, json.dumps(seed_artists), json.dumps(rec_names),
        rating_relevance, rating_mode_fit, rating_explanation, comment,
        datetime.now().isoformat(), user_id,
    ))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM sessions").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def init_track_feedback():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS track_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            mode TEXT,
            track_name TEXT,
            artist TEXT,
            feedback TEXT,
            timestamp TEXT,
            user_id TEXT
        )
    """)
    _ensure_column(conn, "track_feedback", "user_id", "TEXT")  # migrate old databases
    conn.commit()
    conn.close()


def save_track_feedback(session_id, mode, track_name, artist, feedback, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO track_feedback (session_id, mode, track_name, artist, feedback,
                                    timestamp, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session_id, mode, track_name, artist, feedback,
          datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()


def get_all_track_feedback():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM track_feedback").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Accounts (optional sign-in) ─────────────────────────────────────────────

def init_users():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


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

    conn = sqlite3.connect(DB_PATH)
    try:
        exists = conn.execute(
            "SELECT 1 FROM users WHERE username = ? COLLATE NOCASE", (username,)
        ).fetchone()
        if exists:
            return False, "That username is already taken."

        user_id = str(uuid.uuid4())
        salt = os.urandom(16).hex()
        pw_hash = _hash_password(password, salt)
        conn.execute(
            "INSERT INTO users (user_id, username, password_hash, salt, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, username, pw_hash, salt, datetime.now().isoformat()),
        )
        conn.commit()
        return True, user_id
    finally:
        conn.close()


def authenticate(username, password):
    """Return user_id on success, or None on failure."""
    username = (username or "").strip()
    conn = sqlite3.connect(DB_PATH)
    try:
        row = conn.execute(
            "SELECT user_id, password_hash, salt FROM users "
            "WHERE username = ? COLLATE NOCASE", (username,)
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    user_id, stored_hash, salt = row
    if _hash_password(password, salt) == stored_hash:
        return user_id
    return None


def get_username(user_id):
    conn = sqlite3.connect(DB_PATH)
    try:
        row = conn.execute(
            "SELECT username FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    finally:
        conn.close()
    return row[0] if row else None


def get_user_liked_artists(user_id, limit=20):
    """Artists a signed-in user has liked before, most-liked first.
    Used to personalise recommendations for returning users."""
    if not user_id:
        return []
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT artist, COUNT(*) AS c FROM track_feedback "
            "WHERE user_id = ? AND LOWER(feedback) = 'like' AND artist IS NOT NULL "
            "GROUP BY artist ORDER BY c DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    finally:
        conn.close()
    return [r[0] for r in rows]


if __name__ == "__main__":
    init_db()
    init_track_feedback()
    init_users()
    print("Database initialised at", DB_PATH)
    # quick self-test
    sid = new_session_id()
    save_session(sid, "Focus", ["Radiohead"], [{"name": "Test", "artist": "X"}],
                 5, 4, 5, "good")
    print("Saved test session:", sid)
    print("Total sessions:", len(get_all_sessions()))
