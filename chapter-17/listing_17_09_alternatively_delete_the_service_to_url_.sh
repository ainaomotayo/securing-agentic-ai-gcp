#!/usr/bin/env bash
# Alternatively, delete the service-to-url mapping so new requests cannot reach it
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Agent Engine: suspend the deployment by revoking caller permissions
# (The Agent Engine resource itself cannot be "paused", but removing
# roles/aiplatform.user from all callers stops inbound requests)
gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="allUsers" \
  --role="roles/aiplatform.user"

# For service-account-authenticated callers:
gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:frontend-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
