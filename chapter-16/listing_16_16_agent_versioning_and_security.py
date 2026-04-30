#!/usr/bin/env python3
"""
Agent Versioning and Security
Chapter 16 — Secure Deployment

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import vertexai
from vertexai.agent_engines import get as get_agent_engine

# List all deployed versions and delete all but current
old_agent = vertexai.agent_engines.get(
    "projects/123456789/locations/us-central1/reasoningEngines/OLD_RESOURCE_ID"
)
old_agent.delete(force=True)
