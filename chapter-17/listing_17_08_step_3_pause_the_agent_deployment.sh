#!/usr/bin/env bash
# Step 3: Pause the Agent Deployment
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Cloud Run: redirect all traffic to a zero-instance revision (effectively pauses the service)
gcloud run services update-traffic billing-agent-service \
  --to-revisions=LATEST=0 \
  --region=us-central1

# Alternatively, delete the service-to-url mapping so new requests cannot reach it
gcloud run services update billing-agent-service \
  --ingress=internal \
  --region=us-central1
