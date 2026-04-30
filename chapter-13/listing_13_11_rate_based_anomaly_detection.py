#!/usr/bin/env python3
"""
Rate-Based Anomaly Detection
Chapter 13 — Observability Events Audit

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import hashlib
import logging
from typing import Optional, Dict, Any
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext
import google.cloud.logging

cloud_client = google.cloud.logging.Client()
anomaly_logger = cloud_client.logger("adk-agent-anomaly")

TOOL_CALL_ANOMALY_THRESHOLD = 20  # Per invocation


def _hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]


def anomaly_detection_before_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    """Count tool calls per invocation and alert on anomalous frequency."""
    tool_name = tool.name if hasattr(tool, "name") else str(tool)
    count_key = f"temp:tool_call_count:{tool_name}"

    # Increment the per-invocation counter
    current_count = tool_context.state.get(count_key, 0) + 1
    tool_context.state[count_key] = current_count

    if current_count > TOOL_CALL_ANOMALY_THRESHOLD:
        invocation_id = tool_context.invocation_id
        session = tool_context.invocation_context.session

        anomaly_logger.log_struct({
            "anomaly_type": "tool_call_frequency",
            "tool_name": tool_name,
            "call_count": current_count,
            "threshold": TOOL_CALL_ANOMALY_THRESHOLD,
            "invocation_id": invocation_id,
            "session_id": session.id,
            "user_id_token": _hash_user_id(session.user_id),
            "agent_name": tool_context.agent_name,
        }, severity="WARNING")

        # Option 1: Alert and allow (non-blocking detection)
        # Option 2: Block after threshold (defense-in-depth)
        if current_count > TOOL_CALL_ANOMALY_THRESHOLD * 2:
            return {
                "error": "Tool call frequency limit exceeded. Invocation terminated.",
                "anomaly": True,
            }

    return None  # Allow the call
