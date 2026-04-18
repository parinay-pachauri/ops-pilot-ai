import os

from google.adk.agents import Agent

from app.tools.calendar_mcp import cancel_event, create_event, list_events, update_event

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

schedule_agent = Agent(
    model=MODEL,
    name="schedule_agent",
    description="Specialist agent for events, meeting schedules, and calendar updates.",
    instruction="""
You are the scheduling specialist.
Use your tools to create, update, cancel, and list events.
When time assumptions are needed, clearly mention them in your response.
Always preserve user intent and summarize the calendar changes made.
""",
    tools=[create_event, list_events, update_event, cancel_event],
)
