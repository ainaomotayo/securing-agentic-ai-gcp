#!/usr/bin/env bash
# Creating a Dedicated Service Account with Minimum Permissions
# Chapter 04 — Agent Identity And Iam
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Step 1: Create the service account
gcloud iam service-accounts create research-agent-prod \
  --display-name="Research Agent (Production)" \
  --description="Service account for the market research ADK agent" \
  --project=my-project

# Step 2: Grant minimum required roles
# BigQuery read access for the specific dataset
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:research-agent-prod@my-project.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer" \
  --condition="expression=resource.name.startsWith('projects/my-project/datasets/market_data'),title=market-data-only"

# BigQuery job execution (required to run queries)
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:research-agent-prod@my-project.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

# Cloud Storage write access for results bucket only
gsutil iam ch \
  serviceAccount:research-agent-prod@my-project.iam.gserviceaccount.com:roles/storage.objectCreator \
  gs://research-agent-results-prod

# Secret Manager access for API credentials
gcloud secrets add-iam-policy-binding external-api-key \
  --member="serviceAccount:research-agent-prod@my-project.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=my-project

# Step 3: Bind to Cloud Run deployment
gcloud run deploy research-agent \
  --service-account=research-agent-prod@my-project.iam.gserviceaccount.com \
  --region=us-central1 \
  --project=my-project \
  # ... other deployment flags
