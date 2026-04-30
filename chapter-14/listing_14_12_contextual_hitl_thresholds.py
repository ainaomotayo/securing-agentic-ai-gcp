#!/usr/bin/env python3
"""
Contextual HITL Thresholds
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

def set_session_risk_profile(
    tool_context: ToolContext,
    user_role: str,
    transaction_value_usd: float,
) -> None:
    """Set the session's risk level in temp: state based on context."""
    risk_level = "normal"

    if user_role in ("admin", "finance_director"):
        risk_level = "elevated"  # Privileged operations: stricter HITL
    if transaction_value_usd > 50000:
        risk_level = "high"  # Large transactions: stricter HITL
    if transaction_value_usd > 100000:
        risk_level = "critical"  # Very large: multi-party approval required

    tool_context.state["temp:session_risk_level"] = risk_level
