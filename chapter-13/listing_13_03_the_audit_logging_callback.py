#!/usr/bin/env python3
"""
The Audit Logging Callback
Chapter 13 — Observability Events Audit

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import hashlib
import json
import logging
import time
from typing import Optional, Any, Dict
import google.cloud.logging
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

# Initialize Cloud Logging structured logger
cloud_logging_client = google.cloud.logging.Client()
audit_logger = cloud_logging_client.logger("adk-agent-audit")

# PII patterns to redact from logged argument hashes
PII_ARG_KEYS = {"email", "phone", "ssn", "card_number", "password", "secret", "token"}


def _hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]


def _hash_args(args: dict) -> str:
    """Hash tool arguments after redacting PII keys."""
    safe_args = {
        k: "[REDACTED]" if k.lower() in PII_ARG_KEYS else v
        for k, v in args.items()
    }
    args_str = json.dumps(safe_args, sort_keys=True)
    return "sha256:" + hashlib.sha256(args_str.encode()).hexdigest()[:16]


def _get_agent_identity() -> str:
    """Return the current process's service account identity."""
    import os
    return os.environ.get("AGENT_SERVICE_ACCOUNT", "unknown")


def audit_after_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Any,
) -> Optional[Any]:
    """Emit a structured audit record after every tool call."""
    session = tool_context.session
    invocation_id = tool_context.invocation_id

    # Determine outcome from response
    if isinstance(tool_response, dict):
        outcome = "error" if "error" in tool_response else "success"
        error_code = tool_response.get("error_code")
    else:
        outcome = "success"
        error_code = None

    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "invocation_id": invocation_id,
        "agent_name": tool_context.agent_name,
        "agent_identity": _get_agent_identity(),
        "user_id_token": _hash_user_id(session.user_id),
        "session_id": session.id,
        "event_type": "tool_call",
        "tool_name": tool.name if hasattr(tool, "name") else str(tool),
        "args_hash": _hash_args(args),
        "outcome": outcome,
        "error_code": error_code,
    }

    audit_logger.log_struct(record, severity="INFO")
    return None  # Do not modify the tool response


def audit_after_model(
    callback_context: CallbackContext,
    llm_response,
) -> Optional[Any]:
    """Emit a structured audit record after every model call."""
    session = callback_context.session
    invocation_id = callback_context.invocation_id

    function_calls = []
    if llm_response and llm_response.content:
        for part in llm_response.content.parts:
            if hasattr(part, "function_call") and part.function_call:
                function_calls.append(part.function_call.name)

    has_error = bool(
        hasattr(llm_response, "error_code") and llm_response.error_code
    )

    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "invocation_id": invocation_id,
        "agent_name": callback_context.agent_name,
        "agent_identity": _get_agent_identity(),
        "user_id_token": _hash_user_id(session.user_id),
        "session_id": session.id,
        "event_type": "model_call",
        "tool_calls_requested": function_calls,
        "outcome": "error" if has_error else "success",
        "error_code": getattr(llm_response, "error_code", None),
    }

    audit_logger.log_struct(record, severity="INFO")
    return None  # Do not modify the model response
