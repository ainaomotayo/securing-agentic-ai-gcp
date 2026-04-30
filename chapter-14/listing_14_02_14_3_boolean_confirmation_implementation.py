#!/usr/bin/env python3
"""
14.3 Boolean Confirmation: Implementation
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

async def confirmation_threshold(
    amount: int, tool_context
) -> bool:
    """Returns true if the amount is greater than 1000."""
    return amount > 1000

root_agent = Agent(
    # ...
    tools=[
        FunctionTool(reimburse, require_confirmation=confirmation_threshold),
    ],
    # ...
)
