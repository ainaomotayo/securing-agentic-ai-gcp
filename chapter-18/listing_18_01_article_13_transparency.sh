#!/usr/bin/env bash
# Article 13: Transparency
# Chapter 18 — Governance Compliance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Article 13 transparency report for a specific user interaction
INVOCATION_ID="inv-e8f2a1c4-9d3b-4f7e-8c01-2b5a6d9e3f1a"

gcloud logging read \
  "resource.type=cloud_run_revision \
   AND jsonPayload.invocation_id=\"$INVOCATION_ID\"" \
  --project=$PROJECT_ID \
  --format=json | \
  jq '[.[] | {
    timestamp: .timestamp,
    step: .jsonPayload.event_type,
    agent: .jsonPayload.agent_name,
    action: .jsonPayload.tool_name,
    outcome: .jsonPayload.outcome,
    state_keys_modified: .jsonPayload.state_delta_keys
  }]' > article-13-transparency-report.json
