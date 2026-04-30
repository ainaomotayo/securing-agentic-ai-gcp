#!/usr/bin/env bash
# Cloud Armor for Public-Facing Agents
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Create a Cloud Armor security policy
gcloud compute security-policies create agent-armor-policy \
  --description="Security policy for public agent endpoints"

# Block known malicious IP ranges (Managed Protection ruleset)
gcloud compute security-policies rules create 1000 \
  --security-policy=agent-armor-policy \
  --action=deny-403 \
  --expression="evaluatePreconfiguredExpr('xss-stable')"

# Rate limit: max 100 requests per minute per IP
gcloud compute security-policies rules create 2000 \
  --security-policy=agent-armor-policy \
  --action=throttle \
  --rate-limit-threshold-count=100 \
  --rate-limit-threshold-interval-sec=60 \
  --conform-action=allow \
  --exceed-action=deny-429 \
  --enforce-on-key=IP \
  --expression="true"

# Attach to the load balancer backend service
gcloud compute backend-services update agent-backend-service \
  --security-policy=agent-armor-policy \
  --global
