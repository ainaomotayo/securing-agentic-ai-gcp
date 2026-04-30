#!/usr/bin/env python3
"""
The Attribution Gap and Its Compensation
Chapter 04 — Agent Identity And Iam

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from typing import Dict, Any, Optional
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
import logging
import json
import hashlib

logger = logging.getLogger(__name__)

def audit_after_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Dict,
) -> Optional[Dict]:
    """Log tool execution with user attribution for compliance."""
    # User ID comes from the session, set by your application layer
    user_id_raw = tool_context.state.get("user:user_id", "unknown")
    # Hash the user ID before logging to avoid PII in log infrastructure
    user_id_hash = hashlib.sha256(user_id_raw.encode()).hexdigest()[:16]

    audit_entry = {
        "agent_identity": "research-agent-prod@my-project.iam.gserviceaccount.com",
        "user_id_hash": user_id_hash,
        "agent_name": tool_context.agent_name,
        "invocation_id": str(tool_context.invocation_id),
        "tool_name": tool.name,
        "outcome": "success" if not isinstance(tool_response, Exception) else "error",
    }
    # Emit as structured JSON to Cloud Logging
    logger.info(json.dumps(audit_entry))
    return None  # None means: use the original tool_response unchanged
