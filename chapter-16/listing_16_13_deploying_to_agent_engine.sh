#!/usr/bin/env bash
# Deploying to Agent Engine
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# Note: adk deploy agent_engine does not support --service_account.
# Set the runtime service account via the Vertex AI Python SDK or
# an --agent_engine_config_file after deployment.

set -euo pipefail

adk deploy agent_engine \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --display_name="Financial Data Agent" \
  financial_data_agent
