import sqlite3
import json
import uuid
from datetime import datetime

DB_PATH = "music_rec.db"

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
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def new_session_id():
    return str(uuid.uuid4())

def save_session(session_id, mode, seed_artists, recommendations,
                 rating_relevance, rating_mode_fit, rating_explanation, comment):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rec_names = [f"{r['name']} - {r['artist']}" for r in recommendations]
    c.execute("""
        INSERT OR REPLACE INTO sessions
        (session_id, mode, seed_artists, recommendations,
         rating_relevance, rating_mode_fit, rating_explanation, comment, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id, mode, json.dumps(seed_artists), json.dumps(rec_names),
        rating_relevance, rating_mode_fit, rating_explanation, comment,
        datetime.now().isoformat(),
    ))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM sessions").fetchall()
    conn.close()
    return [dict(r) for r in rows]

if __name__ == "__main__":
    init_db()
    print("Database initialised at", DB_PATH)
    # quick self-test
    sid = new_session_id()
    save_session(sid, "Focus", ["Radiohead"], [{"name": "Test", "artist": "X"}], 5, 4, 5, "good")
    print("Saved test session:", sid)
    print("Total sessions:", len(get_all_sessions()))
