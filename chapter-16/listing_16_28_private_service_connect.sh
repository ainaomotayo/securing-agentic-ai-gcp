#!/usr/bin/env bash
# Private Service Connect
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Create a PSC endpoint for Vertex AI
gcloud compute addresses create vertex-ai-psc-ip \
  --global \
  --purpose=PRIVATE_SERVICE_CONNECT \
  --addresses=10.100.0.5 \
  --network=agent-vpc

gcloud compute forwarding-rules create vertex-ai-psc-endpoint \
  --global \
  --network=agent-vpc \
  --address=vertex-ai-psc-ip \
  --target-google-apis-bundle=all-apis
