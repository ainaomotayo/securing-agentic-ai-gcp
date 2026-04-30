#!/usr/bin/env python3
"""
Memory Service Residency
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

memory_service = VertexAiMemoryBankService(
    project="your-gcp-project-id",
    location="europe-west1",  # Memory corpus location
    agent_engine_id=agent_engine_id
)
