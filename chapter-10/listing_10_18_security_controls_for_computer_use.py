#!/usr/bin/env python3
"""
Security Controls for Computer Use
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext
from typing import Dict, Any, Optional

IRREVERSIBLE_BROWSER_ACTIONS = ["submit_form", "confirm_purchase", "delete_account"]

def computer_use_hitl_callback(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[Dict]:
    if tool.name in IRREVERSIBLE_BROWSER_ACTIONS:
        # Escalate to HITL queue; see Chapter 14 pattern
        return {
            "hitl_required": True,
            "action": tool.name,
            "args": args,
            "message": f"Human approval required before {tool.name}."
        }
    return None
