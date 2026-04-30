#!/usr/bin/env bash
# Quarterly Access Review
# Chapter 18 — Governance Compliance
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Quarterly access review script for all registered agents
for AGENT in $(jq -r '.[].agent_id' agent-registry.json); do
  SA=$(jq -r --arg id "$AGENT" '.[] | select(.agent_id == $id) | .service_account' agent-registry.json)
  TOOLS=$(jq -r --arg id "$AGENT" '.[] | select(.agent_id == $id) | .tool_manifest[]' agent-registry.json)
  EXPECTED_ROLES=$(jq -r --arg id "$AGENT" '.[] | select(.agent_id == $id) | .iam_roles[]' agent-registry.json)

  # Get actual roles
  ACTUAL_ROLES=$(gcloud projects get-iam-policy $PROJECT_ID \
    --flatten="bindings[].members" \
    --format='value(bindings.role)' \
    --filter="bindings.members:$SA" | sort)

  echo "Agent: $AGENT"
  diff <(echo "$EXPECTED_ROLES" | sort) <(echo "$ACTUAL_ROLES") && \
    echo "  IAM: COMPLIANT" || \
    echo "  IAM: DRIFT DETECTED - review required"
done
