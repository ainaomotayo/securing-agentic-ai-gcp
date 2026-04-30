#!/usr/bin/env python3
"""
Correct Pattern: Secret Manager
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.cloud import secretmanager


def access_secret(secret_resource_name: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_resource_name)
    return response.payload.data.decode("utf-8")
