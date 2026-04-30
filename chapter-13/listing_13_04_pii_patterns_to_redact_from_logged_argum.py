#!/usr/bin/env python3
"""
PII patterns to redact from logged argument hashes
Chapter 13 — Observability Events Audit

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="pricing_data_agent",
    model="gemini-flash-latest",
    instruction="Retrieve pricing data for the requested items.",
    tools=[get_current_price, get_historical_prices],
    after_tool_callback=audit_after_tool,
    after_model_callback=audit_after_model,
)
