from __future__ import annotations

from typing import Optional

from .db import get_connection, rows_to_dicts, init_db

init_db()


def create_event(
    title: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
    attendees: str = "",
) -> dict:
    """Create a calendar event in the structured event database."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO events (title, description, start_time, end_time, location, attendees, status)
            VALUES (?, ?, ?, ?, ?, ?, 'scheduled')
            """,
            (title, description, start_time, end_time, location, attendees),
        )
        event_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    return {"created": True, "event": dict(row)}


def list_events(status: str = "scheduled") -> dict:
    """List events, defaulting to scheduled items."""
    query = "SELECT * FROM events"
    params: list[str] = []
    if status:
        query += " WHERE status = ?"
        params.append(status.lower())
    query += " ORDER BY start_time"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return {"events": rows_to_dicts(rows), "count": len(rows)}


def update_event(
    event_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """Update selected fields for an event."""
    updates = []
    params: list[object] = []
    for field, value in {
        "title": title,
        "description": description,
        "start_time": start_time,
        "end_time": end_time,
        "location": location,
        "attendees": attendees,
        "status": status.lower() if isinstance(status, str) else status,
    }.items():
        if value is not None:
            updates.append(f"{field} = ?")
            params.append(value)

    if not updates:
        return {"updated": False, "message": "No fields provided to update."}

    params.append(event_id)
    with get_connection() as conn:
        conn.execute(f"UPDATE events SET {', '.join(updates)} WHERE id = ?", params)
        row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()

    if row is None:
        return {"updated": False, "message": f"Event {event_id} not found."}
    return {"updated": True, "event": dict(row)}


def cancel_event(event_id: int) -> dict:
    """Cancel an event."""
    return update_event(event_id=event_id, status="cancelled")
