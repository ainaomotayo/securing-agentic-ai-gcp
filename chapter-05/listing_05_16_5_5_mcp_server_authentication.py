#!/usr/bin/env python3
"""
5.5 MCP Server Authentication
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import os
import subprocess
from google.cloud import secretmanager
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams


def get_mcp_auth_token() -> str:
    if mcp_token := os.getenv("MCP_STATIC_TOKEN"):
        # Static token from Secret Manager (via --set-secrets)
        return mcp_token
    # Dynamic token: use the agent's service account identity
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=os.environ["MCP_SERVER_URL"],
        headers={"Authorization": f"Bearer {get_mcp_auth_token()}"}
    ),
)
