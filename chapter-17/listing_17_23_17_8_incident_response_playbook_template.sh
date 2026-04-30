#!/usr/bin/env bash
# 17.8 Incident Response Playbook Template
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# 1. Revoke service account permissions
gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:[agent-sa]@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="[role]"

# 2. Set abused tool to disabled via app: state
# (Operator sets app:disabled_tools = ["[abused-tool-name]"] in Firestore or admin API)

# 3. Pause Cloud Run traffic
gcloud run services update-traffic [service-name] \
  --to-revisions=LATEST=0 \
  --region=[region]

# 4. Export logs to immutable audit bucket
gcloud logging read "..." --format=json > /tmp/incident-logs.json
gsutil cp /tmp/incident-logs.json gs://[project]-incident-archive/...
