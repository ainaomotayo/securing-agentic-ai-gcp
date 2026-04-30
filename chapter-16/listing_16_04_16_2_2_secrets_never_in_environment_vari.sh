#!/usr/bin/env bash
# 16.2.2 Secrets: Never in Environment Variables
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Store each credential as a named secret
echo "$GOOGLE_API_KEY" | gcloud secrets create GOOGLE_API_KEY \
  --project=$PROJECT_ID --data-file=-

echo "$DATABASE_PASSWORD" | gcloud secrets create DB_PASSWORD \
  --project=$PROJECT_ID --data-file=-

echo "$GMAIL_OAUTH_TOKEN" | gcloud secrets create GMAIL_OAUTH_TOKEN \
  --project=$PROJECT_ID --data-file=-

# Grant the agent service account access to each secret individually
for SECRET in GOOGLE_API_KEY DB_PASSWORD GMAIL_OAUTH_TOKEN; do
  gcloud secrets add-iam-policy-binding $SECRET \
    --member="serviceAccount:financial-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor" \
    --project=$PROJECT_ID
done
