#!/usr/bin/env python3
"""
7.4 Hardening Step 3: In-Tool Guardrails
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.sessions import Session

def create_agent_session(user_id: str) -> Session:
    session = session_service.create_session(app_name="customer-support")
    # Set the policy in app: prefixed state; the model cannot modify app: keys
    session.state["app:refund_policy"] = {
        "max_amount": 500.0,
        "allowed_order_statuses": ["delivered", "shipped"],
        "allowed_for_user_id": user_id,
    }
    return session
