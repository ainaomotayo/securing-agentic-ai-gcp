#!/usr/bin/env bash
# VPC Service Controls
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Create the access policy (once per organization)
gcloud access-context-manager policies create \
  --organization=$ORG_ID \
  --title="Agent Perimeter Policy"

# Create the service perimeter
gcloud access-context-manager perimeters create agent-perimeter \
  --policy=$POLICY_ID \
  --title="Agent API Perimeter" \
  --resources=projects/$PROJECT_NUMBER \
  --restricted-services=bigquery.googleapis.com,storage.googleapis.com,aiplatform.googleapis.com \
  --access-levels=accessPolicies/$POLICY_ID/accessLevels/agent_sa_level
