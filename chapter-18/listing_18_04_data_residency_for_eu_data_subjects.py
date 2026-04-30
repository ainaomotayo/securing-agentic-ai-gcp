#!/usr/bin/env python3
"""
Data Residency for EU Data Subjects
Chapter 18 — Governance Compliance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.cloud import firestore

# For GDPR data residency: Firestore in EU regions only
db = firestore.Client(
    project=PROJECT_ID,
    database="(default)",  # Firestore database configured to europe-west1
)
