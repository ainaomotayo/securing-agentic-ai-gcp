#!/usr/bin/env bash
# 16.2.5 Availability as Security
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud run deploy financial-agent \
  --concurrency=10 \
  --timeout=300 \
  --min-instances=1 \
  --max-instances=50 \
  ...
