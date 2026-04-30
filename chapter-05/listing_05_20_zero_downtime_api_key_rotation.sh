#!/usr/bin/env bash
# Zero-Downtime API Key Rotation
# Chapter 05 — Authentication Patterns
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Step 1: Add new key as a new version
echo "NEW_API_KEY_VALUE" | gcloud secrets versions add EXTERNAL_API_KEY \
  --project=my-project --data-file=-

# Step 2: Verify the new version works (test deployment or canary)

# Step 3: Disable the old version (keep it for audit, do not destroy immediately)
gcloud secrets versions disable 1 \
  --secret=EXTERNAL_API_KEY \
  --project=my-project
