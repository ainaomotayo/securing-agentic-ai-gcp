#!/usr/bin/env bash
# Grant Memory Bank access only to the specific agent's memory resource
# Chapter 04 — Agent Identity And Iam
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Restrict Storage access to a specific bucket
gcloud storage buckets add-iam-policy-binding gs://${REPORT_BUCKET} \
  --member="serviceAccount:${AGENT_SA}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer" \
  --condition="title=bucket-scope,expression=resource.name.startsWith('projects/_/buckets/${REPORT_BUCKET}')"
