#!/usr/bin/env bash
# Verify the new version is the current "latest"
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud run services update billing-agent-service \
  --region=us-central1 \
  --no-traffic  # Don't route traffic yet; wait for validation
