#!/usr/bin/env bash
# 7.2 Hardening Step 1: Dedicated Service Account
# Chapter 07 — Secure Single Agent Architecture
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud iam service-accounts create customer-support-agent-prod \
  --display-name="Customer Support Agent (Production)"

gcloud secrets add-iam-policy-binding payment-api-key \
  --member="serviceAccount:customer-support-agent-prod@my-project.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud run deploy customer-support-agent \
  --service-account=customer-support-agent-prod@my-project.iam.gserviceaccount.com \
  --region=us-central1
