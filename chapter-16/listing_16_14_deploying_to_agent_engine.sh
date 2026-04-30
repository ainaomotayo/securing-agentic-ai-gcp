#!/usr/bin/env bash
# Deploying to Agent Engine
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# IAM for the human or CI/CD service account performing the deployment
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:cicd-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# IAM for reading secrets during deployment packaging (if agent loads secrets at import time)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:cicd-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
