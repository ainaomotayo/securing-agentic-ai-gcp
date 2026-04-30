#!/usr/bin/env bash
# Configuring Log Retention
# Chapter 13 — Observability Events Audit
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Configure log bucket retention
gcloud logging buckets update adk-audit-logs \
  --location=global \
  --retention-days=365 \
  --project=your-gcp-project-id
