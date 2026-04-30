#!/usr/bin/env bash
# Shadow AI Discovery
# Chapter 18 — Governance Compliance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# List all Cloud Run services in the project
gcloud run services list --project=$PROJECT_ID --format=json | \
  jq '.[].metadata.name' > /tmp/deployed-services.txt

# Compare against the registry
python3 << 'EOF'
import json

with open('/tmp/deployed-services.txt') as f:
    deployed = {line.strip().strip('"') for line in f if line.strip()}

# Load registry (from Firestore or config file)
registered = {agent["deployment"]["service_name"] for agent in agent_registry}

unregistered = deployed - registered
if unregistered:
    print("SHADOW AI DETECTED - Unregistered Cloud Run services:")
    for service in sorted(unregistered):
        print(f"  - {service}")
else:
    print("All deployed services are registered.")
EOF
