#!/usr/bin/env bash
# Running Evaluations
# Chapter 15 — Evaluation Red Teaming
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

adk eval \
    customer_support_agent/ \
    tests/security/adversarial_eval_set.evalset.json \
    --config_file_path=tests/security/eval_config.json \
    --print_detailed_results
