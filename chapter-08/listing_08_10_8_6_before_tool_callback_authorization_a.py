#!/usr/bin/env python3
"""
8.6 Before Tool Callback: Authorization and Validation
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import BaseTool, ToolContext
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Tools that require explicit authorization
HIGH_RISK_TOOLS = {"process_refund", "send_email", "delete_record", "transfer_funds"}

def authorize_before_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[Dict]:
    """Check authorization before executing high-risk tools."""
    tool_name = tool.name

    # High-risk tools require explicit permission in app: state
    if tool_name in HIGH_RISK_TOOLS:
        permitted_tools = tool_context.state.get(
            "app:permitted_tools", []
        )

        if tool_name not in permitted_tools:
            logger.warning(
                "Tool authorization denied",
                extra={
                    "tool": tool_name,
                    "session_id": tool_context.session.id,
                }
            )
            return {
                "error": f"Tool '{tool_name}' is not authorized for this session. "
                         f"Contact your administrator."
            }

        # Validate args for financial tools
        if tool_name == "process_refund":
            amount = args.get("amount", 0)
            max_allowed = tool_context.state.get(
                "app:max_refund", 0
            )
            if amount > max_allowed:
                return {
                    "error": f"Refund amount ${amount:.2f} exceeds authorized "
                             f"maximum of ${max_allowed:.2f}."
                }

    return None  # Authorized: proceed with tool execution
