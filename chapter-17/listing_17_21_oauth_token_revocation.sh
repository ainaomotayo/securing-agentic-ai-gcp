#!/usr/bin/env bash
# OAuth Token Revocation
# Chapter 17 — Incident Response
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Google OAuth token revocation (for tokens issued by the agent's OAuth client)
curl -X POST "https://oauth2.googleapis.com/revoke" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "token=$REFRESH_TOKEN_TO_REVOKE"
