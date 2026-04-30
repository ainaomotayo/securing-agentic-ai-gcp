#!/usr/bin/env python3
"""
The Attribution Gap and Its Compensation
Chapter 04 — Agent Identity And Iam

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import CallbackContext
from google.adk.models import LlmResponse
import logging
import json
import hashlib

logger = logging.getLogger(__name__)

def audit_after_tool(
    callback_context: CallbackContext,
    tool_response
) -> None:
    """Log tool execution with user attribution for compliance."""
    # User ID comes from the session, set by your application layer
    user_id_raw = callback_context.state.get("user:user_id", "unknown")
    # Hash the user ID before logging to avoid PII in log infrastructure
    user_id_hash = hashlib.sha256(user_id_raw.encode()).hexdigest()[:16]

    audit_entry = {
        "agent_identity": "research-agent-prod@my-project.iam.gserviceaccount.com",
        "user_id_hash": user_id_hash,
        "session_id": callback_context.invocation_context.session.id,
        "invocation_id": str(callback_context.invocation_context.invocation_id),
        "tool_name": callback_context.tool_name,
        "outcome": "success" if not isinstance(tool_response, Exception) else "error",
    }
    # Emit as structured JSON to Cloud Logging
    logger.info(json.dumps(audit_entry))
