from .calendar_mcp import list_events
from .notes_mcp import list_notes
from .task_mcp import list_tasks


def get_workspace_snapshot() -> dict:
    """Return a structured snapshot of tasks, events, and notes for grounding answers."""
    return {
        "tasks": list_tasks().get("tasks", []),
        "events": list_events(status="").get("events", []),
        "notes": list_notes().get("notes", []),
    }
