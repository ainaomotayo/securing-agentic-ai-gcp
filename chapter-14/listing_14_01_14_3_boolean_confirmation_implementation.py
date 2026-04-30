#!/usr/bin/env python3
"""
14.3 Boolean Confirmation: Implementation
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

root_agent = Agent(
    # ...
    tools=[
        FunctionTool(reimburse, require_confirmation=True),
    ],
    # ...
)
