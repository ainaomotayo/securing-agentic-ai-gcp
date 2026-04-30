#!/usr/bin/env python3
"""
8.7 After Tool Callback: Result Sanitization
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import BaseTool, ToolContext
from typing import Optional, Dict, Any
from copy import deepcopy
import re
import logging

logger = logging.getLogger(__name__)

# Patterns that suggest adversarial instructions in tool results
TOOL_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(?:previous|all)\s+instructions", re.IGNORECASE),
    re.compile(r"your\s+new\s+(?:task|role|instructions)", re.IGNORECASE),
    re.compile(r"<\s*/?(?:instructions?|system|override)\s*>", re.IGNORECASE),
    re.compile(r"disregard\s+(?:your|all|the)\s+(?:instructions|guidelines)", re.IGNORECASE),
]

# Patterns to scrub from tool results before they reach the model
SENSITIVE_IN_RESULTS = re.compile(
    r"(?:password|secret|api.?key|token|credential)\s*[:=]\s*\S+",
    re.IGNORECASE
)


def sanitize_after_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Dict,
) -> Optional[Dict]:
    """Sanitize tool results before passing to the model."""
    # Convert the result to a string for pattern scanning
    result_str = str(tool_response)

    # Check for injection patterns in tool result
    for pattern in TOOL_INJECTION_PATTERNS:
        if pattern.search(result_str):
            logger.warning(
                "Injection pattern detected in tool result",
                extra={
                    "tool": tool.name,
                    "pattern": pattern.pattern,
                    "session_id": tool_context.session.id,
                }
            )
            # Replace the entire result with a safe summary
            return {
                "result": (
                    f"Tool '{tool.name}' returned data that triggered a security filter. "
                    "The result has been sanitized. Please proceed with caution or "
                    "contact support if this is unexpected."
                ),
                "sanitized": True,
            }

    # Scrub accidental credential exposure in tool results
    if SENSITIVE_IN_RESULTS.search(result_str):
        sanitized = deepcopy(tool_response)
        # Replace the specific result field if present
        if "result" in sanitized and isinstance(sanitized["result"], str):
            sanitized["result"] = SENSITIVE_IN_RESULTS.sub(
                "[CREDENTIAL_REDACTED]", sanitized["result"]
            )
        return sanitized

    return None  # Result is clean: pass through unchanged
