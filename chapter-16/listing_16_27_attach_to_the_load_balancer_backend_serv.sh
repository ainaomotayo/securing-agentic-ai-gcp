#!/usr/bin/env bash
# Attach to the load balancer backend service
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud compute security-policies rules create 2000 \
  --security-policy=agent-armor-policy \
  --action=throttle \
  --rate-limit-threshold-count=20 \
  --rate-limit-threshold-interval-sec=60 \
  --conform-action=allow \
  --exceed-action=deny-429 \
  --enforce-on-key=HTTP-HEADER \
  --enforce-on-key-name="X-Goog-Authenticated-User-Email" \
  --expression="true"
