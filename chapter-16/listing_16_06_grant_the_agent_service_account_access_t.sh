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
  --set-secrets="/secrets/db_password=DB_PASSWORD:latest" \
  ...
