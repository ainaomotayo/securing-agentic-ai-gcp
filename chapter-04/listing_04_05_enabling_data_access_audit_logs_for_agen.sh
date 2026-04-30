#!/usr/bin/env bash
# Enabling Data Access Audit Logs for Agent-Touched Services
# Chapter 04 — Agent Identity And Iam
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Enable Data Access audit logs for Firestore
gcloud projects get-iam-policy my-project --format=json > current-policy.json
# Add the following to the auditConfigs section:
# {
#   "service": "firestore.googleapis.com",
#   "auditLogConfigs": [
#     {"logType": "DATA_READ"},
#     {"logType": "DATA_WRITE"}
#   ]
# }
gcloud projects set-iam-policy my-project current-policy.json
