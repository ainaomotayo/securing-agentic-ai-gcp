#!/usr/bin/env bash
# High-Priority Triggers (Page Immediately)
# Chapter 13 — Observability Events Audit
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Cloud Monitoring alert policy
gcloud alpha monitoring policies create \
  --policy-from-file=alert-injection-block.yaml
