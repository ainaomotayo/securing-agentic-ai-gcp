#!/usr/bin/env python3
"""
Unexpected Transfer Path Detection
Chapter 13 — Observability Events Audit

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import google.cloud.logging
from typing import Optional, Dict, Any
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

cloud_client = google.cloud.logging.Client()
anomaly_logger = cloud_client.logger("adk-agent-anomaly")


def monitor_agent_transfers(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    """Log agent transfer events for anomaly analysis."""
    tool_name = tool.name if hasattr(tool, "name") else str(tool)

    if tool_name != "transfer_to_agent":
        return None

    target_agent = args.get("agent_name", "unknown")
    source_agent = tool_context.agent_name
    invocation_id = tool_context.invocation_id

    # Expected transfer graph (populate from agent architecture)
    EXPECTED_TRANSFERS = {
        "coordinator": {"pricing_agent", "research_agent", "summary_agent"},
        "pricing_agent": set(),  # leaf node
        "research_agent": set(),
        "summary_agent": set(),
    }

    expected = EXPECTED_TRANSFERS.get(source_agent, set())
    is_unexpected = target_agent not in expected

    anomaly_logger.log_struct({
        "event_type": "agent_transfer",
        "source_agent": source_agent,
        "target_agent": target_agent,
        "is_unexpected": is_unexpected,
        "invocation_id": invocation_id,
    }, severity="WARNING" if is_unexpected else "INFO")

    if is_unexpected:
        return {
            "error": f"Transfer to '{target_agent}' is not permitted from '{source_agent}'.",
        }

    return None
