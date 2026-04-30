#!/usr/bin/env python3
"""
12.9 Model-Generated Code Review Before Execution
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import subprocess
import json
import tempfile
import os
from typing import Optional, Any
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext

# bandit severity levels and confidence levels to reject
REJECT_SEVERITY = {"HIGH", "MEDIUM"}
REJECT_CONFIDENCE = {"HIGH"}

def static_analysis_gate(
    callback_context: CallbackContext,
    tool,
    args: dict,
    tool_context: ToolContext,
) -> Optional[dict]:
    """before_tool_callback: run bandit static analysis on generated code."""

    generated_code = args.get("code", "")
    if not generated_code:
        return None

    # Write code to a temp file for bandit to analyze
    with tempfile.NamedTemporaryFile(
        suffix=".py",
        mode="w",
        delete=False,
        dir="/tmp",
    ) as f:
        f.write(generated_code)
        temp_path = f.name

    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-q", temp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode not in (0, 1):
            # bandit returns 1 if issues were found; other codes are errors
            import logging
            logging.error("bandit analysis failed: %s", result.stderr)
            return None  # Fail open: let execution proceed if bandit errors

        findings = json.loads(result.stdout) if result.stdout.strip() else {"results": []}

        high_severity_findings = [
            f for f in findings.get("results", [])
            if f.get("issue_severity", "").upper() in REJECT_SEVERITY
            and f.get("issue_confidence", "").upper() in REJECT_CONFIDENCE
        ]

        if high_severity_findings:
            issues = [
                f"{f['issue_text']} at line {f['line_number']}"
                for f in high_severity_findings
            ]
            import logging
            logging.warning(
                "Static analysis blocked code execution: %s",
                "; ".join(issues),
            )
            return {
                "status": "rejected",
                "reason": f"Code failed static analysis: {'; '.join(issues)}",
                "findings": high_severity_findings,
            }

    finally:
        os.unlink(temp_path)

    return None  # Code passed; allow execution
