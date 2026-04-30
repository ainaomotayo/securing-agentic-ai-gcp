#!/usr/bin/env python3
"""
14.6 Risk-Based HITL: When to Require Approval
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from typing import Optional, Any, Dict
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext, FunctionTool

# Risk classification per tool name
TOOL_RISK_REGISTRY = {
    "get_price": "low",
    "search_invoices": "low",
    "create_draft_invoice": "medium",
    "update_customer_record": "medium",
    "send_email": "high",
    "initiate_wire_transfer": "critical",
    "delete_customer_data": "critical",
    "deploy_to_production": "critical",
}

def risk_based_hitl(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    """before_tool_callback: enforce risk-based HITL thresholds."""
    tool_name = tool.name if hasattr(tool, "name") else ""
    risk_level = TOOL_RISK_REGISTRY.get(tool_name, "medium")

    # Low-risk: no HITL
    if risk_level == "low":
        return None

    # Check if session has elevated risk profile
    session_risk = tool_context.state.get("temp:session_risk_level", "normal")

    if risk_level == "medium" and session_risk == "normal":
        # For medium-risk tools in normal sessions, HITL is configurable
        # Boolean confirmation is sufficient
        return None  # Tool should have require_confirmation=True set at registration

    if risk_level in ("high", "critical"):
        # High and critical: always require advanced confirmation
        # This is enforced at the tool level via request_confirmation
        # This callback just validates the risk level was properly considered
        if not tool_context.tool_confirmation:
            # No confirmation yet; the tool should have requested one
            # If we reach here, the tool bypassed confirmation
            import logging
            logging.error(
                "High-risk tool '%s' invoked without HITL confirmation. Blocking.",
                tool_name,
            )
            return {
                "error": f"Tool '{tool_name}' requires HITL confirmation. Direct invocation blocked.",
            }

    return None
