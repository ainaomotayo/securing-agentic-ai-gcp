#!/usr/bin/env bash
# Adversarial User Simulator
# Chapter 15 — Evaluation Red Teaming
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Create an eval set with conversation scenarios
adk eval_set create customer_support_agent/ adversarial_multi_turn_set

adk eval_set add_eval_case \
  customer_support_agent/ \
  adversarial_multi_turn_set \
  --scenarios_file tests/security/adversarial_scenarios.json \
  --session_input_file tests/security/session_input.json
