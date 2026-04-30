#!/usr/bin/env python3
"""
Item 6: Read-Only Tool Filters for Production
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Database MCP server: read-only in production
db_toolset = McpToolset(
    connection_params=SseConnectionParams(url="https://db-mcp.internal/sse"),
    tool_filter=[
        "query",          # SELECT operations
        "list_tables",    # Schema inspection
        "describe_table", # Column metadata
        # Excluded: insert, update, delete, execute, drop
    ],
)
