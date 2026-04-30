#!/usr/bin/env python3
"""
9.9 A2A Protocol: External Agent Authentication
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.integrations.agent_registry import AgentRegistry
import os

registry = AgentRegistry(
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
)

# Retrieve a verified A2A agent from the registry; identity is managed by the platform
agent_name = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global/agents/REPORTS_AGENT_ID"
reports_agent = registry.get_remote_a2a_agent(agent_name=agent_name)
