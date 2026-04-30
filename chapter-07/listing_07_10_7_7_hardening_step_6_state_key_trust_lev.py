#!/usr/bin/env python3
"""
7.7 Hardening Step 6: State Key Trust Levels
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Application code (sets policy; the model cannot override these)
session.state["app:refund_policy"] = {
    "max_amount": 500.0,
    "allowed_order_statuses": ["delivered", "shipped"],
}
session.state["app:customer_tier"] = "standard"  # From your auth system
session.state["app:session_user_id"] = user_id    # From your auth system

# User-provided data (the model can read and write these, but they are lower trust)
session.state["user:preferred_name"] = "Alex"     # User preference, safe to expose
session.state["user:recent_order_id"] = None      # Will be set as the conversation progresses
