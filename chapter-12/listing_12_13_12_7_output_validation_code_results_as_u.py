#!/usr/bin/env python3
"""
12.7 Output Validation: Code Results as Untrusted Data
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import json
import re
from typing import Optional, Any, Dict
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

# Patterns that signal output injection attempts
OUTPUT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instruction",
    r"system\s+prompt\s*:",
    r"<\s*script",
    r"you\s+are\s+now",
]

def validate_code_execution_output(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Any,
) -> Optional[Any]:
    """after_tool_callback: validate code execution output before it reaches the model."""

    if not isinstance(tool_response, dict):
        return {"error": "Code execution output had unexpected type; rejecting."}

    output_text = tool_response.get("output", "") or tool_response.get("stdout", "")
    error_text = tool_response.get("error", "") or tool_response.get("stderr", "")

    # Check for injection patterns in output
    combined_output = f"{output_text}\n{error_text}".lower()
    for pattern in OUTPUT_INJECTION_PATTERNS:
        if re.search(pattern, combined_output):
            import logging
            logging.warning(
                "Injection pattern detected in code execution output: %s",
                pattern,
            )
            return {
                "output": "[Output redacted: contained suspicious content]",
                "error": "",
                "status": "output_filtered",
            }

    # Enforce output length limit to prevent context flooding
    MAX_OUTPUT_LENGTH = 10_000
    if len(output_text) > MAX_OUTPUT_LENGTH:
        output_text = output_text[:MAX_OUTPUT_LENGTH] + "\n[Output truncated]"

    return {
        "output": output_text,
        "error": error_text,
        "status": tool_response.get("status", "ok"),
    }
