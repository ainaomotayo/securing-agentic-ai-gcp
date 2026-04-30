#!/usr/bin/env bash
# Deploying to Agent Engine
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

adk deploy agent_engine \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --display_name="Financial Data Agent" \
  --service_account=financial-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
  financial_data_agent
