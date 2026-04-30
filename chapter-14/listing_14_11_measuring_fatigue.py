#!/usr/bin/env python3
"""
Measuring Fatigue
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import time
import logging

APPROVAL_AUDIT_LOGGER = logging.getLogger("hitl.audit")

def record_approval_outcome(
    session_id: str,
    tool_name: str,
    approved: bool,
    review_duration_seconds: float,
    reviewer_id: str,
) -> None:
    """Record HITL outcome for fatigue analysis."""
    APPROVAL_AUDIT_LOGGER.info(
        "HITL decision",
        extra={
            "session_id": session_id,
            "tool_name": tool_name,
            "approved": approved,
            "review_duration_seconds": review_duration_seconds,
            "reviewer_id": _hash_reviewer_id(reviewer_id),
        }
    )
    # Alert if review duration is under 5 seconds for a critical-risk tool
    if review_duration_seconds < 5.0 and tool_name in CRITICAL_RISK_TOOLS:
        logging.warning(
            "HITL review for critical tool '%s' completed in %.1f seconds, possible rubber-stamp",
            tool_name,
            review_duration_seconds,
        )
