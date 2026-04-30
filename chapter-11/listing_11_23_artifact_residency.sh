#!/usr/bin/env bash
# Artifact Residency
# Chapter 11 — Session State Memory Data Governance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud storage buckets create gs://your-agent-artifacts-eu \
  --location=europe-west1 \
  --uniform-bucket-level-access \
  --project=your-gcp-project-id
