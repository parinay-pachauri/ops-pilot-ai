from __future__ import annotations

from typing import Optional

from .db import get_connection, rows_to_dicts, init_db

init_db()


def create_task(
    title: str,
    description: str = "",
    due_date: str = "",
    priority: str = "medium",
) -> dict:
    """Create a task in the structured task database."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO tasks (title, description, due_date, priority, status)
            VALUES (?, ?, ?, ?, 'pending')
            """,
            (title, description, due_date, priority.lower()),
        )
        task_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return {"created": True, "task": dict(row)}


def list_tasks(status: str = "", priority: str = "") -> dict:
    """List tasks, optionally filtered by status and priority."""
    clauses = []
    params: list[str] = []
    if status:
        clauses.append("status = ?")
        params.append(status.lower())
    if priority:
        clauses.append("priority = ?")
        params.append(priority.lower())

    query = "SELECT * FROM tasks"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, due_date"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return {"tasks": rows_to_dicts(rows), "count": len(rows)}


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """Update selected fields for a task."""
    updates = []
    params: list[object] = []
    for field, value in {
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority.lower() if isinstance(priority, str) else priority,
        "status": status.lower() if isinstance(status, str) else status,
    }.items():
        if value is not None:
            updates.append(f"{field} = ?")
            params.append(value)

    if not updates:
        return {"updated": False, "message": "No fields provided to update."}

    params.append(task_id)
    with get_connection() as conn:
        conn.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if row is None:
        return {"updated": False, "message": f"Task {task_id} not found."}
    return {"updated": True, "task": dict(row)}


def complete_task(task_id: int) -> dict:
    """Mark a task as completed."""
    return update_task(task_id=task_id, status="completed")
