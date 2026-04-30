#!/usr/bin/env python3
"""
18.5 South Korea AI Basic Act: High-Impact AI
Chapter 18 — Governance Compliance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

async def notify_user_of_ai_involvement(
    tool_context: ToolContext,
    decision_type: str,
    decision_details: dict,
) -> dict:
    """
    Sends a structured notification to the user before an AI-assisted decision
    takes effect. Required by Korea AI Basic Act Article 16 for high-impact decisions.
    """
    notification = {
        "notification_type": "ai_decision_involvement",
        "ai_system": "ADK Financial Agent",
        "decision_type": decision_type,
        "decision_details": decision_details,
        "user_rights": [
            "You have the right to request human review of this decision.",
            "You have the right to request an explanation of the factors considered.",
            "You have the right to object to this decision.",
        ],
        "contact": "ai-decisions@company.com",
    }

    # Surface to the user interface through the agent response
    tool_context.state["user:pending_ai_notification"] = notification

    return {
        "status": "notification_queued",
        "notification_id": str(uuid.uuid4()),
    }
