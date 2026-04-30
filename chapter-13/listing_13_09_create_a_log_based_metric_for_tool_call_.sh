#!/usr/bin/env bash
# Create a log-based metric for tool call frequency
# Chapter 13 — Observability Events Audit
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud logging metrics create adk_model_error_rate \
  --description="ADK agent model call error rate" \
  --log-filter='logName="projects/your-project/logs/adk-agent-audit"
    jsonPayload.event_type="model_call"
    jsonPayload.outcome="error"'
