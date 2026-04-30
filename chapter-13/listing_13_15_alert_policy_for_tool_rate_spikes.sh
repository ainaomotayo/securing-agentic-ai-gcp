#!/usr/bin/env bash
# Alert Policy for Tool Rate Spikes
# Chapter 13 — Observability Events Audit
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

gcloud alpha monitoring policies create \
  --policy-from-file=alert-tool-rate-spike.yaml
