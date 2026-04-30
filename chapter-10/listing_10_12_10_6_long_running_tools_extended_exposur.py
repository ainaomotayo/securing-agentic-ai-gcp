#!/usr/bin/env python3
"""
10.6 Long-Running Tools: Extended Exposure Window
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import FunctionTool, ToolContext
import logging

logger = logging.getLogger(__name__)

def start_data_export(
    export_config: dict,
    tool_context: ToolContext,
) -> dict:
    """Start an async data export job. Returns job ID for polling."""
    try:
        job_id = export_service.start_export(export_config)

        # Store the job ID for cleanup if the session is interrupted
        tool_context.invocation_context.session.state["temp:active_export_job"] = job_id

        return {"job_id": job_id, "status": "started"}

    except Exception as exc:
        logger.error(f"Export start failed: {exc}")
        return {"error": "Export service unavailable."}


def check_export_status(job_id: str, tool_context: ToolContext) -> dict:
    """Poll an export job. Cleans up if the job is complete."""
    status = export_service.get_status(job_id)

    if status in ("completed", "failed", "cancelled"):
        # Clear the active job from state; no longer needs cleanup
        tool_context.invocation_context.session.state.pop("temp:active_export_job", None)

    return {"job_id": job_id, "status": status}
