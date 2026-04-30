#!/usr/bin/env bash
# Billing Budget as a DoS Mitigation
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Set a billing budget with email alert at 80% and 100% of expected monthly cost
gcloud billing budgets create \
  --billing-account=$BILLING_ACCOUNT_ID \
  --display-name="Financial Agent Monthly Cap" \
  --budget-amount=500USD \
  --threshold-rule=percent=80 \
  --threshold-rule=percent=100 \
  --filter-projects=projects/$PROJECT_ID \
  --filter-services=services/aiplatform.googleapis.com
