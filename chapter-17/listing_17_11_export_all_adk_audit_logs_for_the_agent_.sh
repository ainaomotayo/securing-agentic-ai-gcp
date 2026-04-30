#!/usr/bin/env bash
# Export all ADK audit logs for the agent during the incident window
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Copy to an immutable audit bucket (Object Lifecycle set to prevent deletion)
gsutil cp /tmp/incident-adk-logs.json \
  gs://$PROJECT_ID-incident-archive/$(date +%Y%m%d-%H%M%S)-billing-agent/
