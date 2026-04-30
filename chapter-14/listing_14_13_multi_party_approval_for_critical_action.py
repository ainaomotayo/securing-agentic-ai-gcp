#!/usr/bin/env python3
"""
Multi-Party Approval for Critical Actions
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

def initiate_critical_infrastructure_change(
    change_description: str,
    affected_systems: list[str],
    tool_context: ToolContext,
) -> dict:
    """Infrastructure change requiring two-party approval."""
    tool_confirmation = tool_context.tool_confirmation

    if not tool_confirmation:
        # First approval request
        tool_context.request_confirmation(
            hint=f"""
INFRASTRUCTURE CHANGE: PRIMARY APPROVAL REQUIRED

Change: {change_description}
Systems affected: {', '.join(affected_systems)}
Irreversible: YES

This change requires approval from TWO engineers.
You are the FIRST reviewer. Your approval triggers the second review.
""",
            payload={
                "first_approval": False,
                "first_reviewer_notes": "",
            },
        )
        return {"status": "Pending first approval"}

    first_approval = tool_confirmation.payload.get("first_approval", False)
    if not first_approval:
        return {"status": "Rejected by first reviewer"}

    # Check if second approval has been obtained
    second_approved = tool_context.state.get(
        f"temp:second_approval:{change_description[:20]}", False
    )
    if not second_approved:
        # Route to second reviewer (different person)
        # This requires the remote confirmation flow from Section 14.5
        return {
            "status": "Pending second approval",
            "first_reviewer_notes": tool_confirmation.payload.get("first_reviewer_notes", ""),
        }

    return _execute_infrastructure_change(change_description, affected_systems)
