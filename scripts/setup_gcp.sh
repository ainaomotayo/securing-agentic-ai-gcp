#!/usr/bin/env bash
# setup_gcp.sh — Creates the minimum GCP resources needed to run book examples.
# Requires: gcloud CLI authenticated, PROJECT_ID environment variable set.
#
# Usage:
#   export PROJECT_ID=your-gcp-project-id
#   bash scripts/setup_gcp.sh

set -euo pipefail

if [[ -z "${PROJECT_ID:-}" ]]; then
  echo "ERROR: PROJECT_ID environment variable not set."
  echo "Usage: export PROJECT_ID=your-project && bash scripts/setup_gcp.sh"
  exit 1
fi

echo "Setting up GCP project: $PROJECT_ID"

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  logging.googleapis.com \
  run.googleapis.com \
  --project="$PROJECT_ID"

echo ""
echo "APIs enabled. Create a service account per chapter README for least-privilege setup."
echo "See Chapter 4 for the full IAM configuration walkthrough."
