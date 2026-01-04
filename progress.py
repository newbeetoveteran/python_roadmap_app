import sqlite3
from datetime import datetime, timedelta

DB = "users.db"

def get_db():
    return sqlite3.connect(DB, check_same_thread=False)

def create_progress_table():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            username TEXT,
            day INTEGER,
            date TEXT,
            completed INTEGER,
            PRIMARY KEY (username, day)
        )
        """)

# ✅ SET completion explicitly (NO TOGGLE)
def set_day_completion(username, day, date, completed):
    with get_db() as conn:
        conn.execute("""
        INSERT INTO progress (username, day, date, completed)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(username, day)
        DO UPDATE SET completed=excluded.completed
        """, (username, day, date, int(completed)))

def is_completed(username, day):
    with get_db() as conn:
        row = conn.execute(
            "SELECT completed FROM progress WHERE username=? AND day=?",
            (username, day)
        ).fetchone()
        return row is not None and row[0] == 1

def completion_stats(username, total_days):
    with get_db() as conn:
        done = conn.execute(
            """
            SELECT COUNT(*) FROM progress
            WHERE username=? AND completed=1
            """,
            (username,)
        ).fetchone()[0]

    return done, done / total_days if total_days else 0

def streak_count(username):
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT date FROM progress
            WHERE username=? AND completed=1
            """,
            (username,)
        ).fetchall()

    dates = sorted(
        {datetime.fromisoformat(r[0]).date() for r in rows},
        reverse=True
    )

    streak = 0
    today = datetime.today().date()

    for d in dates:
        if d == today - timedelta(days=streak):
            streak += 1
        else:
            break

    return streak
