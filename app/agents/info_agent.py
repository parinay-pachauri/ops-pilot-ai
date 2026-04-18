import os

from google.adk.agents import Agent

from app.tools.info_tools import get_workspace_snapshot

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

info_agent = Agent(
    model=MODEL,
    name="info_agent",
    description="Specialist agent for answering questions grounded in stored tasks, events, and notes.",
    instruction="""
You are the information specialist.
Use the workspace snapshot tool to inspect stored tasks, events, and notes.
Answer clearly using the structured data you retrieve.
If the information is missing, say so instead of inventing it.
""",
    tools=[get_workspace_snapshot],
)
