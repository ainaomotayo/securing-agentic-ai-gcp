#!/usr/bin/env bash
# gVisor Isolation in Job Mode
# Chapter 12 — Secure Code Execution
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud container node-pools create code-execution-pool \
  --cluster=your-cluster \
  --sandbox="type=gvisor" \
  --machine-type=n2-standard-4 \
  --num-nodes=2 \
  --project=your-gcp-project-id
