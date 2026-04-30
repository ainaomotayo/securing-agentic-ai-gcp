#!/usr/bin/env python3
"""
10.8 A Secure Tool Wrapper Pattern
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import FunctionTool, ToolContext
from typing import Any, Dict, Optional
from functools import wraps
import logging
import json
import hashlib
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def secure_tool(tool_name: str, max_input_length: int = 1000):
    """
    Decorator that adds standard security properties to any ADK tool function:
    - Input validation (length)
    - Error sanitization (no internal details in tool response)
    - Audit logging
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, tool_context: Optional[ToolContext] = None, **kwargs) -> dict:
            session_id = (
                tool_context.invocation_context.session.id
                if tool_context else "no-session"
            )

            # Check total length of string arguments
            for key, val in kwargs.items():
                if isinstance(val, str) and len(val) > max_input_length:
                    return {"error": f"Input '{key}' exceeds maximum allowed length."}

            # Audit: log before execution
            logger.info(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": "tool_call_start",
                "tool": tool_name,
                "args_hash": hashlib.sha256(str(kwargs).encode()).hexdigest()[:16],
                "session_id": session_id,
            }))

            try:
                if tool_context:
                    result = func(*args, tool_context=tool_context, **kwargs)
                else:
                    result = func(*args, **kwargs)

                logger.info(json.dumps({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": "tool_call_complete",
                    "tool": tool_name,
                    "session_id": session_id,
                }))
                return result

            except Exception as exc:
                logger.error(
                    f"Tool {tool_name} failed: {exc}",
                    exc_info=True,
                    extra={"session_id": session_id}
                )
                # Never expose the raw exception to the model
                return {
                    "error": f"The {tool_name} operation is temporarily unavailable. "
                             "Please try again later or contact support."
                }

        return wrapper
    return decorator


# Usage: apply the decorator to any tool function
@secure_tool(tool_name="send_report_email", max_input_length=500)
def send_report_email(
    recipient: str,
    subject: str,
    body: str,
    tool_context: ToolContext,
) -> dict:
    # This code runs after the security wrapper has validated input and set up logging
    # The wrapper handles error sanitization; exceptions here produce safe error messages
    return email_service.send(recipient=recipient, subject=subject, body=body)
