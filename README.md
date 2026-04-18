# OpsPilot AI

OpsPilot AI is a multi-agent ADK project for managing tasks, schedules, and notes from a single API.

## Features
- Primary orchestrator agent with four specialist sub-agents
- Structured data persisted in SQLite
- Multi-step workflow execution
- API-based deployment on Cloud Run using ADK

## Project structure

```text
ops-pilot-ai/
├── app/
│   ├── agents/
│   └── tools/
├── ops_pilot_agent/
│   ├── agent.py
│   ├── agent.json
│   └── requirements.txt
└── .env.example
```

## Local setup

```bash
python3 -m pip install --upgrade google-adk google-genai a2a-sdk
export PATH=$PATH:/home/$USER/.local/bin
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_CLOUD_LOCATION=us-central1
export MODEL=gemini-2.5-flash
adk web
```

Then select `ops_pilot_agent` in the ADK UI.

## Cloud Run deployment

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com

PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
BUILD_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$BUILD_SA" \
  --role="roles/run.builder"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$BUILD_SA" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$BUILD_SA" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$BUILD_SA" \
  --role="roles/aiplatform.user"

adk deploy cloud_run \
  --project "$PROJECT_ID" \
  --region us-central1 \
  --service_name ops-pilot-ai \
  --a2a \
  ops_pilot_agent

gcloud run services update ops-pilot-ai \
  --region us-central1 \
  --set-env-vars="GOOGLE_CLOUD_LOCATION=us-central1"
```

## Test the deployed API

```bash
export APP_URL="https://YOUR_SERVICE_URL.run.app"

curl -X POST "$APP_URL/apps/ops_pilot_agent/users/user_123/sessions/session_001" \
  -H "Content-Type: application/json" \
  -d '{}'

curl -X POST "$APP_URL/run_sse" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "ops_pilot_agent",
    "user_id": "user_123",
    "session_id": "session_001",
    "new_message": {
      "role": "user",
      "parts": [
        {"text": "Create a design review event tomorrow at 3 PM for 1 hour, add two follow-up tasks, and save a short note."}
      ]
    },
    "streaming": false
  }'
```

## Example prompts
- Create three high-priority tasks for my product launch next Friday.
- Schedule a team sync tomorrow at 4 PM for 30 minutes and list my pending tasks.
- Save a note titled Sprint Review and then create tasks from the action items.
- What are my current tasks, meetings, and notes related to launch?
