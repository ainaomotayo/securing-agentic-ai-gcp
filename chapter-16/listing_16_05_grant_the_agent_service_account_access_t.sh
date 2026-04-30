#!/usr/bin/env bash
# Grant the agent service account access to each secret individually
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud run deploy financial-agent \
  --image=gcr.io/$PROJECT_ID/financial-agent:latest \
  --region=us-central1 \
  --service-account=financial-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-secrets="GOOGLE_API_KEY=GOOGLE_API_KEY:latest,DB_PASSWORD=DB_PASSWORD:latest" \
  --no-allow-unauthenticated \
  --ingress=internal
