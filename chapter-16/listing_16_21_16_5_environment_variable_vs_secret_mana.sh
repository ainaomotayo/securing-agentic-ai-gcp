#!/usr/bin/env bash
# 16.5 Environment Variable vs Secret Manager Decision Matrix
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

> export GOOGLE_CLOUD_PROJECT=your-project-id
> export GOOGLE_CLOUD_LOCATION=us-central1
> export GOOGLE_GENAI_USE_VERTEXAI=True
> 