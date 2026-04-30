#!/usr/bin/env bash
# Restrict Storage access to a specific bucket
# Chapter 04 — Agent Identity And Iam
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

pip install "google-adk[agent-identity]"   # for MCP toolsets via AgentRegistry
pip install "google-adk[a2a]"              # for get_remote_a2a_agent
