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

billing_agent = LlmAgent(
    name="BillingAgent",
    description="Handles invoice retrieval and account balance queries.",
    model="gemini-2.0-flash",
    instruction="Answer billing questions. Do not perform write operations.",
    tools=[get_invoice, get_balance],  # read-only tools
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

support_agent = LlmAgent(
    name="SupportAgent",
    description="Handles account issues and technical support requests.",
    model="gemini-2.0-flash",
    instruction="Resolve support requests. Escalate to human if unresolved.",
    tools=[lookup_ticket, create_ticket],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="""Route requests to the appropriate specialist:
    - Billing questions: BillingAgent
    - Support issues: SupportAgent
    Never combine actions across specialists in a single delegation.""",
    sub_agents=[billing_agent, support_agent],  # explicit, bounded delegation
)
