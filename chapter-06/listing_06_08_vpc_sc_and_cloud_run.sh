#!/usr/bin/env bash
# VPC-SC and Cloud Run
# Chapter 06 — Zero Trust Architecture
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud run services update calendar-agent \
  --vpc-connector=projects/my-project/locations/us-central1/connectors/agent-connector \
  --vpc-egress=all-traffic \
  --project=my-project \
  --region=us-central1
