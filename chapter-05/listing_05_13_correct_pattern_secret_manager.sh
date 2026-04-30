#!/usr/bin/env bash
# Correct Pattern: Secret Manager
# Chapter 05 — Authentication Patterns
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

adk deploy cloud_run \
  --project=my-project \
  --region=us-central1 \
  --service_name=calendar-agent \
  --set-secrets="CALENDAR_CLIENT_SECRET=CALENDAR_CLIENT_SECRET:latest" \
  ./calendar_agent/
