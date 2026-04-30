#!/usr/bin/env bash
# Revoke all bindings (repeat for each role listed above)
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:billing-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/editor"
