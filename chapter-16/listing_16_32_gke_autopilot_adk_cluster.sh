#!/bin/bash
# Securing Agentic AI on Google Cloud
# Chapter 16 — Secure Deployment
# Listing: GKE Autopilot cluster creation + Workload Identity binding for ADK agents
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# Workload Identity Federation is enabled automatically on Autopilot clusters.
# No --workload-pool flag is required or accepted on create-auto.

# Create an Autopilot cluster with Binary Authorization
gcloud container clusters create-auto adk-production \
  --region=us-central1 \
  --project=$PROJECT_ID \
  --binauthz-evaluation-mode=PROJECT_SINGLETON_POLICY_ENFORCE

# Confirm Autopilot is enabled (output: Autopilot: Enabled)
gcloud container clusters describe adk-production \
  --region=us-central1 \
  --format="value(autopilot.enabled)"

# Create the Google service account for the agent
gcloud iam service-accounts create adk-agent-sa \
  --display-name="ADK Agent Service Account" \
  --project=$PROJECT_ID

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:adk-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Create the Kubernetes service account
kubectl create serviceaccount adk-agent-ksa \
  --namespace=adk-agents

# Bind via Workload Identity
gcloud iam service-accounts add-iam-policy-binding \
  adk-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:$PROJECT_ID.svc.id.goog[adk-agents/adk-agent-ksa]"

kubectl annotate serviceaccount adk-agent-ksa \
  --namespace=adk-agents \
  iam.gke.io/gcp-service-account=adk-agent-sa@$PROJECT_ID.iam.gserviceaccount.com
