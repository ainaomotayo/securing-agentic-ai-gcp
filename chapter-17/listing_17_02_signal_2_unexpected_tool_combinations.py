#!/usr/bin/env python3
"""
Signal 2: Unexpected Tool Combinations
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import json
import logging
import google.cloud.logging
from typing import Dict, Any, Optional
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

cloud_client = google.cloud.logging.Client()
anomaly_logger = cloud_client.logger("adk-agent-anomaly")

# In before_tool_callback: detect suspicious tool sequences
SUSPICIOUS_SEQUENCES = [
    ("read_database", "send_external_http"),
    ("list_files", "write_to_webhook"),
    ("get_user_data", "send_email_bulk"),
]

def detect_suspicious_tool_sequence(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    last_tool = tool_context.state.get("temp:last_tool_called")
    current_pair = (last_tool, tool.name) if last_tool else None

    if current_pair in SUSPICIOUS_SEQUENCES:
        logging.getLogger("security").warning(json.dumps({
            "event_type": "suspicious_tool_sequence",
            "invocation_id": tool_context.invocation_id,
            "sequence": list(current_pair),
            "severity": "HIGH",
        }))

    tool_context.state["temp:last_tool_called"] = tool.name
    return None
