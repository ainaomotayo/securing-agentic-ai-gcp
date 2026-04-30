#!/usr/bin/env python3
"""
Resume Configuration
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

def initiate_wire_transfer_idempotent(
    invoice_id: str,
    amount_usd: float,
    tool_context: ToolContext,
) -> dict:
    """Idempotent payment initiation, safe to call more than once."""
    # Check if this invoice was already processed
    completed_key = f"temp:payment_completed:{invoice_id}"
    if tool_context.state.get(completed_key):
        return {"status": "already_processed", "invoice_id": invoice_id}

    # ... HITL confirmation logic ...

    # Mark as completed before returning
    tool_context.state[completed_key] = True
    return {"status": "transferred", "invoice_id": invoice_id}
