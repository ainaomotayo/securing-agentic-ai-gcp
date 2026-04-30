#!/usr/bin/env bash
# Scaffold and Deploy
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Navigate to the parent of your agent directory
cd your-project-directory/

# Scaffold deployment artifacts for Agent Engine
agents-cli scaffold enhance --deployment-target agent_engine

# Authenticate to Google Cloud
gcloud auth application-default login
gcloud config set project your-project-id

# Deploy
agents-cli deploy
