#!/usr/bin/env python3
"""
The Anti-Pattern: Model-Enforced Policy in Session State
Chapter 06 — Zero Trust Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# WRONG: storing authorization policy in no-prefix state that the model reads
session.state["authorized_actions"] = ["read_record", "create_appointment"]

# Agent instruction:
instruction = """Read the authorized_actions list from session state.
Only perform actions in the authorized_actions list."""
