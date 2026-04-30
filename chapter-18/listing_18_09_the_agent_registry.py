#!/usr/bin/env python3
"""
The Agent Registry
Chapter 18 — Governance Compliance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.integrations.agent_registry import AgentRegistry
import os

registry = AgentRegistry(
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
)

# Discover registered MCP servers and A2A agents at runtime
mcp_server_name = f"projects/{project_id}/locations/global/mcpServers/BILLING_MCP_ID"
billing_toolset = registry.get_mcp_toolset(mcp_server_name)

agent_name = f"projects/{project_id}/locations/global/agents/REPORTS_AGENT_ID"
reports_agent = registry.get_remote_a2a_agent(agent_name=agent_name)
