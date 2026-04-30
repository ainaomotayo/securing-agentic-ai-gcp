#!/usr/bin/env python3
"""
Item 1: Authentication Headers for Remote MCP Connections
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.cloud import secretmanager

def get_mcp_token() -> str:
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(
        name="projects/my-project/secrets/mcp-server-token/versions/latest"
    )
    return response.payload.data.decode("UTF-8")

# Remote MCP connection with authentication, not anonymous
mcp_toolset = McpToolset(
    connection_params=SseConnectionParams(
        url="https://mcp.internal.example.com/sse",
        headers={
            "Authorization": f"Bearer {get_mcp_token()}",
            # Additional context headers for audit trail
            "X-ADK-Agent": "research-agent-prod",
            "X-ADK-Project": "my-project",
        },
    ),
    tool_filter=["fetch_news", "search_news"],  # See Item 3
)
