#!/usr/bin/env python3
"""
7.4 Hardening Step 3: In-Tool Guardrails
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import ToolContext

def process_refund(
    order_id: str,
    amount: float,
    tool_context: ToolContext
) -> dict:
    """Process a refund. Amount is subject to policy limits from session state."""

    # Policy comes from app: prefixed state, set by application code, not by the model
    policy = tool_context.invocation_context.session.state.get("app:refund_policy", {})

    max_amount = policy.get("max_amount", 0)  # Default to 0 if policy not set (fail closed)
    allowed_statuses = policy.get("allowed_order_statuses", [])

    # Enforce the policy ceiling; the model cannot override this check
    if amount > max_amount:
        return {
            "error": f"Refund amount ${amount:.2f} exceeds the maximum allowed "
                     f"amount of ${max_amount:.2f}. Please contact support for larger refunds."
        }

    if amount <= 0:
        return {"error": "Refund amount must be greater than zero."}

    # In production: look up the order status before proceeding
    # order = orders_db.get(order_id)
    # if order.status not in allowed_statuses:
    #     return {"error": f"Order {order_id} is not eligible for refund."}

    return {
        "status": "refund_processed",
        "order_id": order_id,
        "amount": amount
    }
