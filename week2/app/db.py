from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional, Iterator
from contextlib import contextmanager

from .exceptions import DatabaseError, ResourceNotFoundError

# ============================================================================
# Configuration
# ============================================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"

# Connection pooling parameters
DB_TIMEOUT = 5.0
DB_CHECK_SAME_THREAD = False


# ============================================================================
# Lifecycle and Connection Management
# ============================================================================


def ensure_data_directory_exists() -> None:
    """Ensure data directory exists, creating if necessary."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """Create and configure a database connection."""
    ensure_data_directory_exists()
    try:
        connection = sqlite3.connect(
            str(DB_PATH),
            timeout=DB_TIMEOUT,
            check_same_thread=DB_CHECK_SAME_THREAD,
        )
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to connect to database: {exc}")
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def db_transaction() -> Iterator[sqlite3.Connection]:
    """
    Context manager for database transactions.
    Automatically commits on success, rolls back on exception.
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as exc:
        conn.rollback()
        raise DatabaseError(f"Database transaction failed: {exc}") from exc
    finally:
        conn.close()


# ============================================================================
# Database Initialization
# ============================================================================


def init_db() -> None:
    """Initialize database schema on app startup."""
    ensure_data_directory_exists()
    try:
        with db_transaction() as connection:
            _create_schema(connection)
    except DatabaseError as exc:
        raise RuntimeError(f"Failed to initialize database: {exc}") from exc


def _create_schema(connection: sqlite3.Connection) -> None:
    """Create database tables if they don't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )
    except sqlite3.Error as exc:
        raise DatabaseError(f"Schema creation failed: {exc}") from exc


# ============================================================================
# Notes Operations
# ============================================================================



def insert_note(content: str) -> int:
    """Insert a new note and return its id."""
    try:
        with db_transaction() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            return int(cursor.lastrowid)
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to insert note: {exc}") from exc


def list_notes() -> list[sqlite3.Row]:
    """Retrieve all notes ordered by creation date (newest first)."""
    try:
        with db_transaction() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
            return list(cursor.fetchall())
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to list notes: {exc}") from exc


def get_note(note_id: int) -> Optional[sqlite3.Row]:
    """Retrieve a single note by id, or None if not found."""
    try:
        with db_transaction() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            return cursor.fetchone()
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to get note: {exc}") from exc


# ============================================================================
# Action Items Operations
# ============================================================================



def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    """Insert multiple action items and return their ids."""
    try:
        with db_transaction() as connection:
            cursor = connection.cursor()
            ids: list[int] = []
            for item in items:
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item),
                )
                ids.append(int(cursor.lastrowid))
            return ids
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to insert action items: {exc}") from exc


def list_action_items(note_id: Optional[int] = None) -> list[sqlite3.Row]:
    """
    Retrieve action items, optionally filtered by note_id.
    Returns items ordered by creation date (newest first).
    """
    try:
        with db_transaction() as connection:
            cursor = connection.cursor()
            if note_id is None:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
                )
            else:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
                )
            return list(cursor.fetchall())
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to list action items: {exc}") from exc


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    """Mark an action item as done or undone."""
    try:
        with db_transaction() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
    except sqlite3.Error as exc:
        raise DatabaseError(f"Failed to update action item: {exc}") from exc


