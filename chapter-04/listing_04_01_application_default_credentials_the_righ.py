#!/usr/bin/env python3
"""
Application Default Credentials: The Right Way to Authenticate on Google Cloud
Chapter 04 — Agent Identity And Iam

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# ADC usage in ADK: no key file needed when running on Google Cloud
# The agent's service account (configured at deployment time)
# is picked up automatically by the Google Cloud Python client libraries

from google.cloud import firestore

def get_customer_data(customer_id: str, tool_context) -> dict:
    # This client automatically uses ADC: no explicit credential configuration
    db = firestore.Client()
    doc = db.collection("customers").document(customer_id).get()
    return doc.to_dict() if doc.exists else {}
