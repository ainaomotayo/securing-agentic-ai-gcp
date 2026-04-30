#!/usr/bin/env python3
"""
Item 5: Restrictive File Paths for Filesystem MCP Servers
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import os

ALLOWED_PATH = os.path.dirname(os.path.abspath(__file__))

filesystem_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                ALLOWED_PATH,  # Restricts access to this directory and below
            ],
        )
    ),
    tool_filter=["read_file", "list_directory"],  # read-only operations only
)
