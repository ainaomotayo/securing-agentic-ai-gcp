#!/usr/bin/env bash
# Step 1: Revoke the Agent's Service Account Permissions
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# List the current bindings for the agent service account
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:serviceAccount:billing-agent-sa@$PROJECT_ID.iam.gserviceaccount.com"

# Revoke all bindings (repeat for each role listed above)
gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:billing-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:billing-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/billing.admin"  # This should never have been granted
