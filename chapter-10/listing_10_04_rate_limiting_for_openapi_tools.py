#!/usr/bin/env python3
"""
Rate Limiting for OpenAPI Tools
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import BaseTool, ToolContext
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

TOOL_RATE_LIMITS = {
    "external_api_search": {"calls_per_minute": 10, "calls_per_hour": 100},
    "external_api_enrich": {"calls_per_minute": 5, "calls_per_hour": 50},
}

def rate_limit_before_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[Dict]:
    """Enforce per-tool rate limits using temp: state."""
    rate_config = TOOL_RATE_LIMITS.get(tool.name)
    if not rate_config:
        return None  # Tool not rate-limited

    state = tool_context.invocation_context.session.state
    rate_key = f"temp:rate_{tool.name}"
    now = datetime.utcnow()

    rate_data = state.get(rate_key, {"calls": [], "hourly_calls": []})

    # Clean expired entries
    minute_ago = now - timedelta(minutes=1)
    hour_ago = now - timedelta(hours=1)
    rate_data["calls"] = [t for t in rate_data["calls"] if datetime.fromisoformat(t) > minute_ago]
    rate_data["hourly_calls"] = [t for t in rate_data["hourly_calls"] if datetime.fromisoformat(t) > hour_ago]

    if len(rate_data["calls"]) >= rate_config["calls_per_minute"]:
        logger.warning(f"Rate limit exceeded for {tool.name}")
        return {"error": f"Rate limit reached for {tool.name}. Please retry in 60 seconds."}

    if len(rate_data["hourly_calls"]) >= rate_config["calls_per_hour"]:
        return {"error": f"Hourly rate limit reached for {tool.name}. Please retry later."}

    # Record this call
    rate_data["calls"].append(now.isoformat())
    rate_data["hourly_calls"].append(now.isoformat())
    state[rate_key] = rate_data

    return None  # Proceed with the tool call
