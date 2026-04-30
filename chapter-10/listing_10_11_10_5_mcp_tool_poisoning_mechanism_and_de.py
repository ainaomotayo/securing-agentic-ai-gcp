#!/usr/bin/env python3
"""
10.5 MCP Tool Poisoning: Mechanism and Defense
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.mcp_tool import McpToolset
import re

DESCRIPTION_INJECTION_PATTERNS = [
    re.compile(r"always\s+(?:call|invoke|use)", re.IGNORECASE),
    re.compile(r"after\s+(?:this|every|each)\s+(?:call|operation)", re.IGNORECASE),
    re.compile(r"ignore\s+(?:previous|all)\s+instructions", re.IGNORECASE),
    re.compile(r"your\s+new\s+(?:task|role|instructions)", re.IGNORECASE),
]

def validate_tool_descriptions(tools: list) -> bool:
    """Screen MCP tool descriptions for injection patterns."""
    for tool in tools:
        description = getattr(tool, "description", "") or ""
        for pattern in DESCRIPTION_INJECTION_PATTERNS:
            if pattern.search(description):
                return False  # Reject the entire toolset
    return True
