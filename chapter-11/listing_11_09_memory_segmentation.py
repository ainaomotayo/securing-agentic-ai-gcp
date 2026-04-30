#!/usr/bin/env python3
"""
Memory Segmentation
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google import adk
from google.adk.memory import VertexAiMemoryBankService

# Two memory services: one for conversation history, one for authoritative policy
conversation_memory = VertexAiMemoryBankService(
    project=PROJECT,
    location=LOCATION,
    agent_engine_id=CONVERSATION_ENGINE_ID
)

policy_memory = VertexAiMemoryBankService(
    project=PROJECT,
    location=LOCATION,
    agent_engine_id=POLICY_ENGINE_ID  # Write-protected; only populated by CI pipeline
)
