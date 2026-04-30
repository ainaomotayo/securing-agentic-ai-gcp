#!/usr/bin/env python3
"""
14.4 Advanced Confirmation: Designing the Approval Payload
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

def request_time_off(days: int, tool_context):
    """Request day off for the employee."""
    tool_confirmation = tool_context.tool_confirmation
    if not tool_confirmation:
        tool_context.request_confirmation(
            hint=(
                'Please approve or reject the tool call request_time_off() by'
                ' responding with a FunctionResponse with an expected'
                ' ToolConfirmation payload.'
            ),
            payload={
                'approved_days': 0,
            },
        )
        return {'status': 'Manager approval is required.'}

    approved_days = tool_confirmation.payload['approved_days']
    approved_days = min(approved_days, days)
    if approved_days == 0:
        return {'status': 'The time off request is rejected.', 'approved_days': 0}
    return {
        'status': 'ok',
        'approved_days': approved_days,
    }
