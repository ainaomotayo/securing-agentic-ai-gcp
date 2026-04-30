#!/usr/bin/env bash
# 16.2.1 Service Account: Never Use the Default
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Create the service account
gcloud iam service-accounts create financial-agent-sa \
  --display-name="Financial Agent Service Account" \
  --project=$PROJECT_ID

# Grant only the permissions this specific agent's tools require
# Tool: BigQuery read-only queries
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:financial-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

# Tool: Secret Manager access for credentials
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:financial-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# ADK agent to Vertex AI (for model calls)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:financial-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Deploy with explicit service account
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --service_name=financial-agent \
  $AGENT_PATH \
  -- \
  --service-account=financial-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --no-allow-unauthenticated
