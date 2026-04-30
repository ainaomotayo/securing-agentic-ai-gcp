#!/usr/bin/env bash
# 16.2 Cloud Run: Complete Security Configuration
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

> adk deploy cloud_run \
>   --project=$GOOGLE_CLOUD_PROJECT \
>   --region=$GOOGLE_CLOUD_LOCATION \
>   $AGENT_PATH
> 