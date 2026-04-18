from __future__ import annotations

from .db import get_connection, rows_to_dicts, init_db

init_db()


def save_note(title: str, content: str, tags: str = "") -> dict:
    """Save a note to the structured notes database."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO notes (title, content, tags) VALUES (?, ?, ?)",
            (title, content, tags),
        )
        note_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return {"saved": True, "note": dict(row)}


def list_notes(tag: str = "") -> dict:
    """List notes, optionally filtered by tag text."""
    query = "SELECT * FROM notes"
    params: list[str] = []
    if tag:
        query += " WHERE tags LIKE ?"
        params.append(f"%{tag}%")
    query += " ORDER BY created_at DESC"
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return {"notes": rows_to_dicts(rows), "count": len(rows)}


def search_notes(query: str) -> dict:
    """Search notes by title or content."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM notes
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
            ORDER BY created_at DESC
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        ).fetchall()
    return {"notes": rows_to_dicts(rows), "count": len(rows)}
