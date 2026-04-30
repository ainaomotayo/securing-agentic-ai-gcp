#!/usr/bin/env python3
"""
Configuring Explicit Transfer Restrictions
Chapter 06 — Zero Trust Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import LlmAgent

intake_agent = LlmAgent(
    name="IntakeAgent",
    model="gemini-2.0-flash",
    instruction="Process the patient intake form and extract structured data.",
    # Explicit: this agent must not transfer to any other agent
    # It only processes the form and returns structured output
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
