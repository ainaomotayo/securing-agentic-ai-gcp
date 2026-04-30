#!/usr/bin/env bash
# Session State Residency
# Chapter 11 — Session State Memory Data Governance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud firestore databases create \
  --location=europe-west1 \
  --type=firestore-native \
  --project=your-gcp-project-id
