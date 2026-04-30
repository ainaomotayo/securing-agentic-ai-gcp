#!/usr/bin/env python3
"""
Patterns that suggest injection attempts
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="customer_support_agent",
    instruction=SYSTEM_INSTRUCTION,
    tools=[refund_tool],
    generate_content_config=...,
    before_model_callback=before_model_security_check,
)
