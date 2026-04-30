#!/usr/bin/env python3
"""
Session State Residency
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

session_service = VertexAiSessionService(
    project="your-gcp-project-id",
    location="europe-west1"  # EU data residency
)
