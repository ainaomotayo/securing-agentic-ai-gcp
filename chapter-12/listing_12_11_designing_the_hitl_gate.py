#!/usr/bin/env python3
"""
Designing the HITL Gate
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

# In-memory approval store (use a persistent queue in production)
_pending_approvals: dict[str, asyncio.Future] = {}

async def code_execution_hitl_gate(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    """HITL gate: suspend code execution until a human approves or rejects."""

    generated_code = args.get("code", "")
    if not generated_code:
        return None  # No code to review; let execution proceed

    invocation_id = tool_context.invocation_id
    session_id = tool_context.session.id
    user_id = tool_context.session.user_id

    # Build the approval payload for the reviewer
    approval_payload = {
        "invocation_id": invocation_id,
        "session_id": session_id,
        "user_id": user_id,
        "generated_code": generated_code,
        "code_line_count": len(generated_code.splitlines()),
        "session_state_keys": list(tool_context.state.keys()),
        "review_required": True,
    }

    logger.info(
        "Code execution pending human approval for session %s",
        session_id,
    )

    # Send the payload to the review queue
    # In production: publish to Pub/Sub, write to Firestore, or call HITL API
    await _send_to_review_queue(approval_payload)

    # Wait for the reviewer's decision
    future: asyncio.Future = asyncio.get_event_loop().create_future()
    _pending_approvals[invocation_id] = future

    try:
        decision = await asyncio.wait_for(future, timeout=300.0)  # 5 min timeout
    except asyncio.TimeoutError:
        logger.warning("Code review timed out for session %s; rejecting", session_id)
        return {
            "status": "rejected",
            "reason": "Review timeout. Code execution was not approved within 5 minutes.",
        }
    finally:
        _pending_approvals.pop(invocation_id, None)

    if decision.get("approved"):
        logger.info("Code execution approved for session %s", session_id)
        return None  # Allow execution to proceed
    else:
        return {
            "status": "rejected",
            "reason": decision.get("reason", "Rejected by reviewer."),
        }


async def _send_to_review_queue(payload: dict) -> None:
    """Send code review payload to the approval queue."""
    # Implement: write to Pub/Sub, Firestore, or your HITL platform
    pass


def approve_code_execution(invocation_id: str, approved: bool, reason: str = "") -> None:
    """Called by the reviewer's approval endpoint to resolve the gate."""
    future = _pending_approvals.get(invocation_id)
    if future and not future.done():
        future.set_result({"approved": approved, "reason": reason})
