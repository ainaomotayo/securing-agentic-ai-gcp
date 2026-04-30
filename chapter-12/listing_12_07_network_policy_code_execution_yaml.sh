#!/usr/bin/env bash
# network-policy-code-execution.yaml
# Chapter 12 — Secure Code Execution
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

kubectl apply -f network-policy-code-execution.yaml
