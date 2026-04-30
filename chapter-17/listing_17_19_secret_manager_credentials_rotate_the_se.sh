#!/usr/bin/env bash
# Secret Manager Credentials (Rotate the Secret Version)
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Rotate a compromised API key
NEW_API_KEY="your-new-rotated-api-key"

# Add new version to the existing secret
echo "$NEW_API_KEY" | gcloud secrets versions add THIRD_PARTY_API_KEY \
  --project=$PROJECT_ID \
  --data-file=-

# Disable the old version (not delete; you may need it for forensics)
gcloud secrets versions disable 1 \
  --secret=THIRD_PARTY_API_KEY \
  --project=$PROJECT_ID

# Verify the new version is the current "latest"
gcloud secrets versions list THIRD_PARTY_API_KEY --project=$PROJECT_ID
