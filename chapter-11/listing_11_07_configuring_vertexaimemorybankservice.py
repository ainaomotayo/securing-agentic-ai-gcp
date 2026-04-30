#!/usr/bin/env python3
"""
Configuring VertexAiMemoryBankService
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.memory import VertexAiMemoryBankService
from google import adk

memory_service = VertexAiMemoryBankService(
    project="your-gcp-project-id",
    location="us-central1",
    agent_engine_id=agent_engine_id
)

runner = adk.Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service
)
