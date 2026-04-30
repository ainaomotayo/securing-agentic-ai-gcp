#!/usr/bin/env python3
"""
5.5 MCP Server Authentication
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

if os.getenv("K_SERVICE"):  # Cloud Run environment
    mcp_connection = StreamableHTTPConnectionParams(
        url=os.environ["MCP_SERVER_URL"],
        headers={"Authorization": f"Bearer {get_mcp_auth_token()}"}
    )
else:  # Local development
    mcp_connection = StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        )
    )

mcp_toolset = McpToolset(connection_params=mcp_connection)
