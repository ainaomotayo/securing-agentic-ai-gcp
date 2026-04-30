#!/usr/bin/env bash
# Artifact Deletion and Cleanup
# Chapter 11 — Session State Memory Data Governance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Lifecycle rule: delete objects older than 180 days
gcloud storage buckets update gs://your-agent-artifacts-prod \
  --lifecycle-file=lifecycle.json
