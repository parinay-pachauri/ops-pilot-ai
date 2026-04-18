import os

from google.adk.agents import Agent

from app.tools.task_mcp import complete_task, create_task, list_tasks, update_task

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

task_agent = Agent(
    model=MODEL,
    name="task_agent",
    description="Specialist agent for task creation, updates, completion, and listing.",
    instruction="""
You are the task specialist.
Use your tools to create, list, update, prioritize, and complete tasks.
Always be specific and structured.
When you create tasks from user requests or notes, create concise task titles and useful descriptions.
""",
    tools=[create_task, list_tasks, update_task, complete_task],
)
