#!/usr/bin/env bash
# 16.2.3 Networking: Restrict Ingress and Egress
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Backend agent: internal ingress only
gcloud run deploy financial-agent \
  --ingress=internal \
  --vpc-connector=projects/$PROJECT_ID/locations/us-central1/connectors/agent-vpc-connector \
  --vpc-egress=all-traffic \
  ...
