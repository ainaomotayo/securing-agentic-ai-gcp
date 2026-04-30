#!/usr/bin/env python3
"""
Agent instruction:
Chapter 06 — Zero Trust Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Application code sets policy in app: state at agent startup
# (only application code can write to app: keys)
def before_agent_callback(callback_context):
    user_id = callback_context.state.get("user:authenticated_user_id")
    permissions = fetch_permissions_from_iam(user_id)
    # app: key: only application code writes here
    callback_context.state["app:authorized_actions"] = permissions
    return None  # allow agent to proceed

# Tool enforces the policy by reading from app: state
def validated_record_write(tool_context: ToolContext, action: str, record_id: str) -> dict:
    authorized = tool_context.state.get("app:authorized_actions", [])
    if action not in authorized:
        return {"status": "denied", "reason": f"action {action} not in authorized_actions"}
    # perform write
    return perform_write(action, record_id)
