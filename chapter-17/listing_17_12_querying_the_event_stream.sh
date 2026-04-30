#!/usr/bin/env bash
# Querying the Event Stream
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Find all invocations during the incident window by the billing tool
gcloud logging read \
  "resource.type=cloud_run_revision \
   AND jsonPayload.tool_name=\"write_credit_adjustment\" \
   AND timestamp >= \"2026-04-27T02:47:00Z\"" \
  --project=$PROJECT_ID \
  --format=json | jq '.[].jsonPayload.invocation_id' | sort -u > /tmp/incident_invocations.txt

# For each invocation ID, pull the full event sequence
INVOCATION_ID="inv-e8f2a1c4-9d3b-4f7e-8c01-2b5a6d9e3f1a"
gcloud logging read \
  "resource.type=cloud_run_revision \
   AND jsonPayload.invocation_id=\"$INVOCATION_ID\"" \
  --project=$PROJECT_ID \
  --format=json | jq 'sort_by(.timestamp)' > /tmp/invocation-replay.json
