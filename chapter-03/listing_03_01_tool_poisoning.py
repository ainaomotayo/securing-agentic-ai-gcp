#!/usr/bin/env python3
"""
Tool Poisoning
Chapter 03 — Threat Landscape

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, SseConnectionParams

# Explicit allow-list: only these two tool names will be loaded
# regardless of what the MCP server returns in its manifest
mcp_toolset = McpToolset(
    connection_params=SseConnectionParams(
        url="https://market-data-mcp-server.internal/sse",
        headers={"Authorization": f"Bearer {get_mcp_auth_token()}"},
    ),
    tool_filter=["get_current_price", "get_historical_prices"],
)
