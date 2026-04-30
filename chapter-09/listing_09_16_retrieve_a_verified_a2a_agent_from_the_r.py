#!/usr/bin/env python3
"""
Retrieve a verified A2A agent from the registry; identity is managed by the platform
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Even with registry-verified identity, treat A2A agent outputs as external data.
# Apply after_tool_callback sanitization to any AgentTool wrapping an A2A agent.

a2a_research_tool = agent_tool.AgentTool(agent=reports_agent)

# The after_tool_callback from Chapter 8 applies here too
