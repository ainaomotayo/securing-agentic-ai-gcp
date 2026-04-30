#!/usr/bin/env bash
# Step 4: Preserve Evidence Before Any Changes
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Export all ADK audit logs for the agent during the incident window
INCIDENT_START="2026-04-27T02:47:00Z"
INCIDENT_END="2026-04-27T03:30:00Z"

gcloud logging read \
  "resource.type=cloud_run_revision \
   AND resource.labels.service_name=billing-agent-service \
   AND timestamp >= \"$INCIDENT_START\" \
   AND timestamp <= \"$INCIDENT_END\"" \
  --project=$PROJECT_ID \
  --format=json \
  > /tmp/incident-adk-logs.json
