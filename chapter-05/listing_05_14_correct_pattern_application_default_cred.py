#!/usr/bin/env python3
"""
Correct Pattern: Application Default Credentials for Google Services
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import google.auth
import google.auth.transport.requests

# No credential object needed, ADC finds the service account from the environment
credentials, project = google.auth.default(
    scopes=["https://www.googleapis.com/auth/bigquery.readonly"]
)
request = google.auth.transport.requests.Request()
credentials.refresh(request)
access_token = credentials.token
