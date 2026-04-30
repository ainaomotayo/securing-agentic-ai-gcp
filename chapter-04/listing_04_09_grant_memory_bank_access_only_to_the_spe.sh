#!/usr/bin/env bash
# Grant Memory Bank access only to the specific agent's memory resource
# Chapter 04 — Agent Identity And Iam
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${AGENT_SA}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer" \
  --condition="expression=request.time.getHours('America/New_York') >= 8 && request.time.getHours('America/New_York') <= 20,title=business-hours-only"
