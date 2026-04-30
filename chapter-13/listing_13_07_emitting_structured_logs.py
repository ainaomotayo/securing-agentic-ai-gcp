#!/usr/bin/env python3
"""
Emitting Structured Logs
Chapter 13 — Observability Events Audit

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import google.cloud.logging

client = google.cloud.logging.Client()
logger = client.logger("adk-agent-audit")

# This record is queryable by any field
logger.log_struct({
    "event_type": "tool_call",
    "tool_name": "get_current_price",
    "invocation_id": invocation_id,
    "outcome": "success",
    "agent_name": "pricing_agent",
}, severity="INFO")
