#!/usr/bin/env python3
"""
7.1 The Insecure Baseline: What ADK Gives You by Default
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def process_refund(order_id: str, amount: float) -> dict:
    """Process a refund for the specified order."""
    # In production this would call a payment system
    return {"status": "refund_processed", "order_id": order_id, "amount": amount}

refund_tool = FunctionTool(func=process_refund)

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="customer_support_agent",
    tools=[refund_tool],
    # No instruction; the model has no behavioral boundary
    # No callbacks; no input or output validation
    # No generate_content_config; no content filters configured
)
