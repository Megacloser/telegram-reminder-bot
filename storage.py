import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "bot_data.db"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    conn = _connect()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS user_languages ("
        "user_id INTEGER PRIMARY KEY, lang TEXT NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS reminders ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "chat_id INTEGER NOT NULL, "
        "text TEXT NOT NULL, "
        "lang TEXT NOT NULL, "
        "due_at REAL NOT NULL)"
    )
    conn.commit()
    conn.close()


def get_language(user_id: int) -> str | None:
    conn = _connect()
    row = conn.execute(
        "SELECT lang FROM user_languages WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return row[0] if row else None


def set_language(user_id: int, lang: str) -> None:
    conn = _connect()
    conn.execute(
        "INSERT INTO user_languages (user_id, lang) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET lang = excluded.lang",
        (user_id, lang),
    )
    conn.commit()
    conn.close()


def add_reminder(chat_id: int, text: str, lang: str, due_at: float) -> int:
    conn = _connect()
    cur = conn.execute(
        "INSERT INTO reminders (chat_id, text, lang, due_at) VALUES (?, ?, ?, ?)",
        (chat_id, text, lang, due_at),
    )
    conn.commit()
    reminder_id = cur.lastrowid
    conn.close()
    return reminder_id


def delete_reminder(reminder_id: int) -> None:
    conn = _connect()
    conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()


def get_pending_reminders() -> list[tuple[int, int, str, str, float]]:
    conn = _connect()
    rows = conn.execute(
        "SELECT id, chat_id, text, lang, due_at FROM reminders"
    ).fetchall()
    conn.close()
    return rows


def get_reminders_by_chat(chat_id: int) -> list[tuple[int, str, str, float]]:
    conn = _connect()
    rows = conn.execute(
        "SELECT id, text, lang, due_at FROM reminders WHERE chat_id = ? ORDER BY due_at ASC",
        (chat_id,),
    ).fetchall()
    conn.close()
    return rows
