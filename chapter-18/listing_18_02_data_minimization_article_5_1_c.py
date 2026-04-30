#!/usr/bin/env python3
"""
Data Minimization (Article 5(1)(c))
Chapter 18 — Governance Compliance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents.callback_context import CallbackContext

def enforce_data_minimization(callback_context: CallbackContext) -> None:
    """After each agent turn, clear PII state keys beyond the minimum retention window."""
    state = callback_context.state

    # Clear PII that should not persist beyond the current session
    transient_pii_keys = [
        k for k in state.keys()
        if k.startswith("user:pii_") and not k.endswith("_retained")
    ]
    for key in transient_pii_keys:
        state[key] = None  # Signals SessionService to clear the value
