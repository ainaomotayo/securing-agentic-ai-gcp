#!/usr/bin/env python3
"""
7.6 Hardening Step 5: Model Armor via Callback
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Conceptual: Chapter 8 covers the full ModelArmorGuard implementation
from my_security_lib import ModelArmorGuard  # organization-defined wrapper

model_armor = ModelArmorGuard(
    project_id="my-project",
    location="us-central1",
    template_name="customer-support-baseline",
)

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="customer_support_agent",
    instruction=SYSTEM_INSTRUCTION,
    tools=[refund_tool],
    generate_content_config=...,
    before_model_callback=model_armor.before_model,
    after_model_callback=model_armor.after_model,
)
