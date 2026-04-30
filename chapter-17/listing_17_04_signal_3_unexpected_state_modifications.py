#!/usr/bin/env python3
"""
Signal 3: Unexpected State Modifications
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

def detect_privileged_state_write(event) -> bool:
    if not event.actions or not event.actions.state_delta:
        return False
    for key in event.actions.state_delta:
        if key.startswith("app:") and event.author != "user":
            return True
    return False
