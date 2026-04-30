#!/usr/bin/env python3
"""
Session Hijacking
Chapter 03 — Threat Landscape

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

mcp_toolset = McpToolset(
    connection_params=SseConnectionParams(
        url="https://mcp-server.internal/sse",
        headers={
            "Authorization": f"Bearer {mcp_auth_token}",
            "X-Agent-Identity": agent_identity_token,
        },
    ),
)
