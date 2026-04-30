#!/usr/bin/env python3
"""
Reconstructing the Action Sequence
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import json
from datetime import datetime

def reconstruct_invocation(log_file: str, invocation_id: str) -> list[dict]:
    with open(log_file) as f:
        entries = json.load(f)

    events = [
        e for e in entries
        if e.get("jsonPayload", {}).get("invocation_id") == invocation_id
    ]
    events.sort(key=lambda e: e["timestamp"])

    sequence = []
    for e in events:
        p = e["jsonPayload"]
        sequence.append({
            "time": e["timestamp"],
            "event_type": p.get("event_type"),
            "agent": p.get("agent_name"),
            "tool": p.get("tool_name"),
            "args_hash": p.get("args_hash"),  # SHA-256 of sanitized args
            "outcome": p.get("outcome"),
            "state_delta_keys": p.get("state_delta_keys", []),
        })

    return sequence
