#!/usr/bin/env python3
"""
Artifact Versioning as an Audit Mechanism
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import ToolContext

async def read_artifact_version(
    filename: str,
    version: int,
    tool_context: ToolContext,
) -> dict:
    artifact = await tool_context.load_artifact(filename=filename, version=version)
    if artifact is None:
        return {"error": f"Version {version} of artifact '{filename}' not found"}

    return {
        "filename": filename,
        "version": version,
        "mime_type": artifact.inline_data.mime_type,
        "size_bytes": len(artifact.inline_data.data)
    }
