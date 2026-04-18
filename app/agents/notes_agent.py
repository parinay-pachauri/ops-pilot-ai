import os

from google.adk.agents import Agent

from app.tools.notes_mcp import list_notes, save_note, search_notes

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

notes_agent = Agent(
    model=MODEL,
    name="notes_agent",
    description="Specialist agent for saving, searching, and summarizing notes.",
    instruction="""
You are the notes specialist.
Use your tools to save notes, retrieve notes, and search prior information.
When a user asks to save notes, preserve key facts and tags.
When a user asks for notes-based context, search before answering.
""",
    tools=[save_note, list_notes, search_notes],
)
