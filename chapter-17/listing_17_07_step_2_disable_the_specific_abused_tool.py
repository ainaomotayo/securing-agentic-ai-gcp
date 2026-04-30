#!/usr/bin/env python3
"""
Step 2: Disable the Specific Abused Tool
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from typing import Dict, Any, Optional
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

# Emergency tool disable via app: state (set by operator, not agent)
def emergency_tool_gate(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    disabled_tools = tool_context.state.get("app:disabled_tools", [])
    if tool.name in disabled_tools:
        return {"error": f"Tool {tool.name} is temporarily disabled by operations."}
    return None

# Operator command to disable the email tool (e.g., via admin API or Cloud Firestore update)
# app:disabled_tools = ["send_email", "send_bulk_email"]
