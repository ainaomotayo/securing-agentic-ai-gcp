#!/usr/bin/env python3
"""
Artifact Namespacing and Path Traversal
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import re
import google.genai.types as types
from google.adk.tools import ToolContext

SAFE_FILENAME_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._\-]{0,127}$")

def save_report_artifact(
    filename: str,
    report_bytes: bytes,
    mime_type: str,
    tool_context: ToolContext,
) -> dict:
    # Validate filename before passing to ArtifactService
    if not SAFE_FILENAME_PATTERN.match(filename):
        return {"error": "Invalid filename. Use only alphanumeric characters, dots, hyphens, and underscores."}

    # Block user: prefix unless the agent explicitly grants cross-session scope
    if filename.startswith("user:"):
        return {"error": "Cross-session artifact scope requires explicit authorization."}

    # Block path separators that could cause traversal
    if "/" in filename or "\\" in filename or ".." in filename:
        return {"error": "Invalid filename: path separators are not permitted."}

    artifact = types.Part(
        inline_data=types.Blob(
            mime_type=mime_type,
            data=report_bytes
        )
    )

    version = tool_context.save_artifact(filename=filename, artifact=artifact)

    return {
        "status": "saved",
        "filename": filename,
        "version": version,
        "mime_type": mime_type
    }
