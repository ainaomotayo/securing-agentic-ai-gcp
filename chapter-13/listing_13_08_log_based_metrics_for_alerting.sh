#!/usr/bin/env bash
# Log-Based Metrics for Alerting
# Chapter 13 — Observability Events Audit
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Create a log-based metric for tool call frequency
gcloud logging metrics create adk_tool_call_rate \
  --description="ADK agent tool call rate per minute" \
  --log-filter='logName="projects/your-project/logs/adk-agent-audit"
    jsonPayload.event_type="tool_call"' \
  --value-extractor="EXTRACT(jsonPayload.agent_name)"
