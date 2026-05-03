#!/bin/bash
# Securing Agentic AI on Google Cloud
# Chapter 6 — Zero Trust Architecture
# Listing: Cloud Armor DDoS and WAF protection for Agent Gateway
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# Prerequisites: Application Load Balancer with agent-gateway-backend backend service.
# Attach this policy to the ALB, not to Agent Gateway directly.

# Create the Cloud Armor policy for the Agent Gateway endpoint
gcloud compute security-policies create agent-gateway-armor \
  --description="DDoS and WAF protection for Agent Gateway"

# Block known injection and XSS patterns at the HTTP layer
gcloud compute security-policies rules create 1000 \
  --security-policy=agent-gateway-armor \
  --action=deny-403 \
  --expression="evaluatePreconfiguredExpr('xss-stable') || evaluatePreconfiguredExpr('sqli-stable')"

# Rate limit: 60 requests per minute per authenticated user identity.
# Agent interactions are conversational; 60 rpm is generous for a human user
# and restrictive for an automated attack.
gcloud compute security-policies rules create 2000 \
  --security-policy=agent-gateway-armor \
  --action=throttle \
  --rate-limit-threshold-count=60 \
  --rate-limit-threshold-interval-sec=60 \
  --conform-action=allow \
  --exceed-action=deny-429 \
  --enforce-on-key=HTTP-HEADER \
  --enforce-on-key-name="X-Goog-Authenticated-User-Email" \
  --expression="true"

# Attach to the backend service fronting Agent Gateway
gcloud compute backend-services update agent-gateway-backend \
  --security-policy=agent-gateway-armor \
  --global
