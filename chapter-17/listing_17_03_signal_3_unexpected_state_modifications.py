#!/usr/bin/env python3
"""
Signal 3: Unexpected State Modifications
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

> if event.actions and event.actions.state_delta:
>     print(f"  State changes: {event.actions.state_delta}")
> 