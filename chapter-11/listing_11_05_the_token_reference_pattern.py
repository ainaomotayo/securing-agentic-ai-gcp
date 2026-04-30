#!/usr/bin/env python3
"""
The Token Reference Pattern
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import re
from google.adk.tools import ToolContext
from google.cloud import secretmanager

def store_user_token_reference(
    user_id: str,
    token: str,
    tool_context: ToolContext,
) -> dict:
    """Store an OAuth token in Secret Manager and record the reference in state."""
    client = secretmanager.SecretManagerServiceClient()
    project = "your-gcp-project-id"

    # Store the actual token in Secret Manager
    secret_name = f"projects/{project}/secrets/user-oauth-{user_id}"

    # Write the Secret Manager path to session state, not the token
    # Use user: prefix so the reference persists across sessions for this user
    tool_context.state[f"user:oauth_secret_ref"] = secret_name
    tool_context.state[f"user:oauth_scopes"] = ["https://www.googleapis.com/auth/calendar.readonly"]

    return {"status": "token_stored", "secret_ref": secret_name}


def retrieve_user_token(tool_context: ToolContext) -> str:
    """Retrieve an OAuth token using the Secret Manager reference from state."""
    secret_ref = tool_context.state.get("user:oauth_secret_ref")
    if not secret_ref:
        raise ValueError("No OAuth token reference found in session state")

    # Validate the reference looks like a Secret Manager path
    if not re.match(r"^projects/[^/]+/secrets/[^/]+$", secret_ref):
        raise ValueError(f"Invalid secret reference format: {secret_ref}")

    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(
        name=f"{secret_ref}/versions/latest"
    )
    return response.payload.data.decode("utf-8")
