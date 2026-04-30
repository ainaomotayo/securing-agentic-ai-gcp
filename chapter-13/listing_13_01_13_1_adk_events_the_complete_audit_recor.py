#!/usr/bin/env python3
"""
13.1 ADK Events: The Complete Audit Record
Chapter 13 — Observability Events Audit

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Conceptual structure of an ADK Event
class Event(LlmResponse):
    author: str          # 'user' or agent name
    invocation_id: str   # ID for the whole interaction run
    id: str              # Unique ID for this specific event
    timestamp: float     # Creation time
    actions: EventActions  # State changes, artifact saves, control signals
    branch: Optional[str]  # Hierarchy path in multi-agent systems
    # From LlmResponse:
    content: Optional[types.Content]  # Function calls, function responses, text
    error_code: Optional[str]
    error_message: Optional[str]
