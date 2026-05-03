#!/bin/bash
# Securing Agentic AI on Google Cloud
# Chapter 17 — Incident Response
# Listing: IAM-restricted forensic archive with object retention (Step 4)
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# Do NOT pseudonymize or redact evidence before archiving.
# Raw forensic data is legal evidence required for GDPR Article 33 notification,
# regulatory investigations, and insurance claims. The control is access restriction,
# not data transformation.

# Create a dedicated forensic archive bucket with object retention (90-day minimum)
gsutil mb -l us-central1 gs://$PROJECT_ID-forensic-archive
gsutil retention set 90d gs://$PROJECT_ID-forensic-archive
gsutil versioning set on gs://$PROJECT_ID-forensic-archive

# Restrict read access: bind to named roles only
gsutil iam ch -d allUsers gs://$PROJECT_ID-forensic-archive
gcloud storage buckets add-iam-policy-binding gs://$PROJECT_ID-forensic-archive \
  --member="group:security-incident-response@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
gcloud storage buckets add-iam-policy-binding gs://$PROJECT_ID-forensic-archive \
  --member="serviceAccount:incident-writer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectCreator"

# Copy to the restricted archive using the dedicated incident-writer service account.
# The agent service account must have been revoked in Step 1 before this step runs.
gsutil cp /tmp/incident-adk-logs.json \
  gs://$PROJECT_ID-forensic-archive/$(date +%Y%m%d-%H%M%S)-billing-agent/raw-logs.json
