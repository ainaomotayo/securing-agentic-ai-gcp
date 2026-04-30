#!/usr/bin/env python3
"""
8.5 After Model Callback: Output Security
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import CallbackContext
from google.adk.models import LlmResponse
from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)

# Patterns to redact from model output before returning to caller
OUTPUT_REDACTION_PATTERNS = {
    "account_number": re.compile(r"\b\d{8,16}\b"),  # 8–16 digit account numbers
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "routing_number": re.compile(r"\b0[0-9]{8}\b"),  # US routing numbers
}

REDACTED_TOKEN = "[REDACTED]"


def pii_redact_after_model(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    """Redact sensitive patterns from model output before returning to caller."""
    if not llm_response.content or not llm_response.content.parts:
        return None

    modified = False
    for part in llm_response.content.parts:
        if not hasattr(part, "text") or not part.text:
            continue

        original_text = part.text
        cleaned_text = original_text

        for pattern_name, pattern in OUTPUT_REDACTION_PATTERNS.items():
            matches = pattern.findall(cleaned_text)
            if matches:
                cleaned_text = pattern.sub(REDACTED_TOKEN, cleaned_text)
                logger.warning(
                    "PII redacted from model output",
                    extra={
                        "pattern": pattern_name,
                        "match_count": len(matches),
                        "session_id": callback_context.state.get("app:session_id"),
                    }
                )
                modified = True

        if modified:
            part.text = cleaned_text

    return llm_response if modified else None
