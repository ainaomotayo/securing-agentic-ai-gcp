#!/usr/bin/env python3
"""
Artifact Residency
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

gcs_service = GcsArtifactService(
    bucket_name="your-agent-artifacts-eu"
)
