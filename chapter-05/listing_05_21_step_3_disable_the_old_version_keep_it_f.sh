#!/usr/bin/env bash
# Step 3: Disable the old version (keep it for audit, do not destroy immediately)
# Chapter 05 — Authentication Patterns
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud run services update calendar-agent \
  --project=my-project \
  --region=us-central1 \
  --tag=latest
# Trigger new instance creation:
gcloud run services update-traffic calendar-agent --to-latest
