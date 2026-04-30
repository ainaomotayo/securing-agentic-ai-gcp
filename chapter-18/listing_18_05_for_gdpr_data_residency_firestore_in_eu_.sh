#!/usr/bin/env bash
# For GDPR data residency: Firestore in EU regions only
# Chapter 18 — Governance Compliance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud run deploy eu-agent-service \
  --region=europe-west1 \
  ...
