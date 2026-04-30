#!/usr/bin/env bash
# 4.5 Workload Identity Federation for GKE Deployments
# Chapter 04 — Agent Identity And Iam
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

# Step 1: Enable Workload Identity on the GKE cluster
gcloud container clusters update my-cluster \
  --workload-pool=my-project.svc.id.goog \
  --region=us-central1

# Step 2: Create the Kubernetes namespace and service account
kubectl create namespace agent-workloads
kubectl create serviceaccount research-agent-ksa \
  --namespace=agent-workloads

# Step 3: Bind the Kubernetes service account to the Google Cloud service account
gcloud iam service-accounts add-iam-policy-binding \
  research-agent-prod@my-project.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:my-project.svc.id.goog[agent-workloads/research-agent-ksa]"

# Step 4: Annotate the Kubernetes service account
kubectl annotate serviceaccount research-agent-ksa \
  --namespace=agent-workloads \
  iam.gke.io/gcp-service-account=research-agent-prod@my-project.iam.gserviceaccount.com
