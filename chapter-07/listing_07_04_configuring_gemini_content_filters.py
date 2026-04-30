#!/usr/bin/env python3
"""
Configuring Gemini Content Filters
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.genai import types

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="customer_support_agent",
    instruction=SYSTEM_INSTRUCTION,
    tools=[refund_tool],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            ),
        ]
    ),
)
