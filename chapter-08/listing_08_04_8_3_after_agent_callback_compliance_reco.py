#!/usr/bin/env python3
"""
8.3 After Agent Callback: Compliance Recording
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import CallbackContext
import logging
import json
import hashlib
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def compliance_after_agent(
    callback_context: CallbackContext,
) -> None:
    """Record compliance-relevant facts about every agent invocation."""
    user_id_raw = callback_context.state.get("app:user_id", "unknown")

    audit_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "invocation_id": str(callback_context.invocation_id),
        "agent_name": callback_context.agent_name,
        "user_id_hash": hashlib.sha256(user_id_raw.encode()).hexdigest()[:16],
        "session_id": callback_context.state.get("app:session_id", "unknown"),
        "event_type": "agent_completion",
    }
    # Structured JSON to Cloud Logging: queryable for compliance reports
    logger.info(json.dumps(audit_record))
