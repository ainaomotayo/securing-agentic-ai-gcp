#!/usr/bin/env bash
# Audit Trail for State and Memory Operations
# Chapter 11 — Session State Memory Data Governance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Enable data access audit logs for Agent Platform
gcloud projects set-iam-policy your-gcp-project-id policy.json
