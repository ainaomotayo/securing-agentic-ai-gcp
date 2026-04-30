#!/usr/bin/env python3
"""
Item 3: Filter MCP Tools Using tool_filter
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Without tool_filter: agent can call every tool the MCP server exposes now or in the future
risky_toolset = McpToolset(
    connection_params=SseConnectionParams(url="https://mcp.example.com/sse"),
    # No tool_filter; all current AND future tools exposed
)

# With tool_filter: agent can only call the tools you have explicitly approved
safe_toolset = McpToolset(
    connection_params=SseConnectionParams(url="https://mcp.example.com/sse"),
    # Explicit allow-list; the attack from the opening scenario fails here
    # because send_report is not in the filter
    tool_filter=["fetch_news", "search_news", "get_categories"],
)
