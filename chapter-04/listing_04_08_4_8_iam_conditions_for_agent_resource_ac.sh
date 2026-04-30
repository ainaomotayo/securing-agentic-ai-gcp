#!/usr/bin/env bash
# 4.8 IAM Conditions for Agent Resource Access
# Chapter 04 — Agent Identity And Iam
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Grant Memory Bank access only to the specific agent's memory resource
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${AGENT_SA}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user" \
  --condition="expression=resource.name.startsWith('projects/${PROJECT_ID}/locations/us-central1/ragCorpora/${AGENT_CORPUS_ID}'),title=agent-corpus-scope"
