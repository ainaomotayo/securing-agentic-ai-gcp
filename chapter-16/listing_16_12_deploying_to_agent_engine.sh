#!/usr/bin/env bash
# Deploying to Agent Engine
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

> PROJECT_ID=my-project-id
> LOCATION_ID=us-central1
>
> adk deploy agent_engine \
>         --project=$PROJECT_ID \
>         --region=$LOCATION_ID \
>         --display_name="My First Agent" \
>         multi_tool_agent
> 