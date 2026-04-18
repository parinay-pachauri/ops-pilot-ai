# OpsPilot AI

OpsPilot AI is a multi-agent productivity assistant built using **Google
ADK** and deployed on **Google Cloud Run**.

## Features

-   AI agent powered by Gemini models
-   Tool integrations for:
    -   Task management
    -   Notes storage
    -   Event scheduling
-   SQLite database for structured storage
-   API-based architecture

## Architecture

User → Cloud Run API → OpsPilot Agent → Tools → SQLite Database

## Tech Stack

-   Google ADK
-   Gemini 2.5 Flash
-   Python
-   SQLite
-   Cloud Run

## Deployment Steps

1.  Enable required services

```{=html}
<!-- -->
```
    gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com

2.  Deploy the agent

```{=html}
<!-- -->
```
    adk deploy cloud_run --project YOUR_PROJECT_ID --region us-central1 --service_name ops-pilot-ai --a2a ops_pilot_agent

3.  Test the agent

Create session

    curl -X POST "$APP_URL/apps/ops_pilot_agent/users/user_123/sessions/session_001"

Run agent

    curl -X POST "$APP_URL/run_sse"

## Example Prompt

    create a task called prepare presentation

## Cloud Run URL

Replace with your deployed URL.

## Demo

Show: - Deployment - API request - Agent tool execution
