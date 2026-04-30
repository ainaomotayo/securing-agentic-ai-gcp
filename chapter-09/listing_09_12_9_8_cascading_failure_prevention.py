#!/usr/bin/env python3
"""
9.8 Cascading Failure Prevention
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import LoopAgent

# LoopAgent with explicit termination conditions
document_review_loop = LoopAgent(
    name="DocumentReviewLoop",
    sub_agents=[reviewer_agent, reviser_agent],
    max_iterations=5,  # Hard ceiling; prevents DoS from unbounded loops
)
