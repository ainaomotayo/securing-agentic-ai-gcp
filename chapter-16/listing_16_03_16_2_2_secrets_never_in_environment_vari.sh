#!/usr/bin/env bash
# 16.2.2 Secrets: Never in Environment Variables
# Chapter 16 — Secure Deployment
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

> echo "<<put your GOOGLE_API_KEY here>>" | gcloud secrets create GOOGLE_API_KEY \
>   --project=my-project \
>   --data-file=-
>
> gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
>   --member="serviceAccount:1234567890-compute@developer.gserviceaccount.com" \
>   --role="roles/secretmanager.secretAccessor" \
>   --project=my-project
> 