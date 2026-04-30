#!/usr/bin/env python3
"""
Handling PII in Session State
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import hashlib

def tokenize_pii(raw_value: str, salt: str) -> str:
    """Replace a PII value with a deterministic token."""
    return hashlib.sha256(f"{salt}{raw_value}".encode()).hexdigest()[:16]

def store_user_contact(
    email: str,
    phone: str,
    tool_context: ToolContext,
) -> dict:
    salt = tool_context.state.get("app:pii_salt", "default-salt")

    # Store tokens, not raw values
    tool_context.state["user:email_token"] = tokenize_pii(email, salt)
    tool_context.state["user:phone_token"] = tokenize_pii(phone, salt)

    # Log the association in a separate PII vault (not session state)
    # pii_vault.store(token=email_token, raw=email, user_id=user_id)

    return {"status": "contact_stored"}
