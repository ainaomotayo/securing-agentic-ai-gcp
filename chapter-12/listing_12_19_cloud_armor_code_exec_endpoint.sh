#!/bin/bash
# Securing Agentic AI on Google Cloud
# Chapter 12 — Secure Code Execution
# Listing: Cloud Armor rate-based-ban protection for code execution endpoint
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# Prerequisites: Application Load Balancer with code-exec-backend backend service.

# Create a security policy for the code execution agent endpoint
gcloud compute security-policies create code-exec-armor-policy \
  --description="DDoS and rate-limit protection for code execution endpoint"

# Block known attack patterns at the WAF layer
gcloud compute security-policies rules create 1000 \
  --security-policy=code-exec-armor-policy \
  --action=deny-403 \
  --expression="evaluatePreconfiguredExpr('xss-stable')"

# Tight rate limit: 10 requests per minute per IP.
# Legitimate users do not submit more than 10 code execution requests per minute.
# An attacker attempting to exhaust GKE Job quota exceeds this immediately.
gcloud compute security-policies rules create 2000 \
  --security-policy=code-exec-armor-policy \
  --action "rate-based-ban" \
  --rate-limit-threshold-count=10 \
  --rate-limit-threshold-interval-sec=60 \
  --ban-duration-sec=300 \
  --conform-action=allow \
  --exceed-action=deny-429 \
  --enforce-on-key=IP \
  --expression="true"

# Attach to the backend service fronting the code execution agent
gcloud compute backend-services update code-exec-backend \
  --security-policy=code-exec-armor-policy \
  --global
