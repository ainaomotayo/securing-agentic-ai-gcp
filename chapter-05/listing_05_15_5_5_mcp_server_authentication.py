#!/usr/bin/env python3
"""
5.5 MCP Server Authentication
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

> McpToolset(
>     connection_params=StreamableHTTPConnectionParams(
>         url="https://your-mcp-server-url.run.app/mcp",
>         headers={"Authorization": "Bearer your-auth-token"}
>     ),
> )
> 