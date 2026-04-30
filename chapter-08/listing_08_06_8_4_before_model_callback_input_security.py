#!/usr/bin/env python3
"""
8.4 Before Model Callback: Input Security
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
from typing import Optional
import re

# PII patterns to scrub from model input
PII_PATTERNS = {
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b"),
    "phone_us": re.compile(r"\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "email": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
}

REPLACEMENT_TOKENS = {
    "ssn": "[SSN_REDACTED]",
    "credit_card": "[CARD_REDACTED]",
    "phone_us": "[PHONE_REDACTED]",
    "email": "[EMAIL_REDACTED]",
}


def pii_scrub_before_model(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Scrub PII from all content in the LLM request before it reaches the model."""
    if not llm_request.contents:
        return None

    modified = False
    for content in llm_request.contents:
        for part in getattr(content, "parts", []):
            if not hasattr(part, "text") or not part.text:
                continue

            original_text = part.text
            cleaned_text = original_text

            for pii_type, pattern in PII_PATTERNS.items():
                replacement = REPLACEMENT_TOKENS[pii_type]
                new_text = pattern.sub(replacement, cleaned_text)
                if new_text != cleaned_text:
                    cleaned_text = new_text
                    modified = True

            if modified:
                part.text = cleaned_text

    return None  # Always allow the (now sanitized) call to proceed
