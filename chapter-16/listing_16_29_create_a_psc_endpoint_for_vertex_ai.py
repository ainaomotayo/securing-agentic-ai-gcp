#!/usr/bin/env python3
"""
Create a PSC endpoint for Vertex AI
Chapter 16 — Secure Deployment

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import vertexai

# Route Vertex AI calls through the PSC endpoint
vertexai.init(
    project=PROJECT_ID,
    location="us-central1",
    api_endpoint="10.100.0.5",  # PSC endpoint IP
)
