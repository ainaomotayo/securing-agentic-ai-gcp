#!/usr/bin/env python3
"""
Security Controls for Computer Use
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

IRREVERSIBLE_BROWSER_ACTIONS = ["submit_form", "confirm_purchase", "delete_account"]

def computer_use_hitl_callback(tool_context, tool_name: str, tool_args: dict) -> dict | None:
    if tool_name in IRREVERSIBLE_BROWSER_ACTIONS:
        # Escalate to HITL queue; see Chapter 14 pattern
        return {
            "hitl_required": True,
            "action": tool_name,
            "args": tool_args,
            "message": f"Human approval required before {tool_name}."
        }
    return None
