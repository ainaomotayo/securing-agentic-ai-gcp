#!/usr/bin/env python3
"""
Per-Server Credentials
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

crm_token = access_secret("projects/my-project/secrets/CRM_MCP_TOKEN/versions/latest")
analytics_token = access_secret("projects/my-project/secrets/ANALYTICS_MCP_TOKEN/versions/latest")

crm_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://crm-mcp.internal.example.com/mcp",
        headers={"Authorization": f"Bearer {crm_token}"}
    ),
)

analytics_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://analytics-mcp.internal.example.com/mcp",
        headers={"Authorization": f"Bearer {analytics_token}"}
    ),
)

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="enterprise_agent",
    tools=[crm_tools, analytics_tools],
)
