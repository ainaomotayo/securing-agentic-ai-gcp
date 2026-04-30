#!/usr/bin/env bash
# Provision Observability Infrastructure
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Enable observability features: prompt-response logging, content logs
agents-cli infra single-project
