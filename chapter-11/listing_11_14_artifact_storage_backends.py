#!/usr/bin/env python3
"""
Artifact Storage Backends
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.artifacts import GcsArtifactService
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="report_agent",
    model="gemini-flash-latest",
    instruction="Generate reports when requested."
)

gcs_service = GcsArtifactService(
    bucket_name="your-agent-artifacts-prod"
)

runner = Runner(
    agent=agent,
    app_name="report_app",
    session_service=VertexAiSessionService(project=PROJECT, location=LOCATION),
    artifact_service=gcs_service
)
