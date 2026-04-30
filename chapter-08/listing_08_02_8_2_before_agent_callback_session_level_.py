#!/usr/bin/env python3
"""
8.2 Before Agent Callback: Session-Level Security
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import CallbackContext
from google.genai import types
from datetime import datetime, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def rate_limit_before_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """Enforce per-user rate limiting at the session level."""
    user_id = callback_context.state.get("app:user_id", "anonymous")
    rate_key = f"app:rate_limit_{user_id}"

    rate_data = callback_context.state.get(rate_key, {
        "count": 0,
        "window_start": datetime.utcnow().isoformat(),
    })

    window_start = datetime.fromisoformat(rate_data["window_start"])
    if datetime.utcnow() - window_start > timedelta(hours=1):
        # Reset the window
        rate_data = {"count": 1, "window_start": datetime.utcnow().isoformat()}
        callback_context.state[rate_key] = rate_data
        return None

    if rate_data["count"] >= 100:  # 100 invocations per hour
        logger.warning("Rate limit exceeded", extra={"user_id": user_id})
        return types.Content(
            role="model",
            parts=[types.Part(text=(
                "You have reached the maximum number of requests for this hour. "
                "Please try again later."
            ))]
        )

    rate_data["count"] += 1
    callback_context.state[rate_key] = rate_data
    return None  # Allow the agent to run
