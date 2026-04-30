#!/usr/bin/env python3
"""
Resume Configuration
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.apps import App, ResumabilityConfig

app = App(
    name="payment_agent",
    root_agent=payment_agent,
    resumability_config=ResumabilityConfig(
        is_resumable=True,
    ),
)
