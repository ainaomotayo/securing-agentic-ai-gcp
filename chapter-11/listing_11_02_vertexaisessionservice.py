#!/usr/bin/env python3
"""
VertexAiSessionService
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.sessions import VertexAiSessionService

session_service = VertexAiSessionService(
    project="your-gcp-project-id",
    location="us-central1"
)
