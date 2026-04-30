#!/usr/bin/env python3
"""
7.5 Hardening Step 4: Callback-Based Input Validation
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from typing import Optional
import re

# Patterns that suggest injection attempts
INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"you\s+are\s+now\s+a?\s+(?:different|new)\s+(?:agent|ai|assistant|bot)",
    r"disregard\s+(?:your|all|the)\s+(?:instructions|guidelines|rules)",
    r"your\s+new\s+(?:task|role|instructions)\s+(?:is|are)",
    r"system\s*:\s*(?:you|ignore|forget)",
    r"<\s*/?(?:instructions?|system|prompt)\s*>",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

MAX_INPUT_LENGTH = 2000  # Characters

def before_model_security_check(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Screen model input for injection patterns and enforce length limits."""

    # Inspect the last user message (the most recent input)
    if llm_request.contents:
        last_content = llm_request.contents[-1]
        if hasattr(last_content, "parts"):
            for part in last_content.parts:
                if hasattr(part, "text") and part.text:
                    user_text = part.text

                    # Length limit: prevent token flooding
                    if len(user_text) > MAX_INPUT_LENGTH:
                        return LlmResponse(
                            content=types.Content(
                                role="model",
                                parts=[types.Part(text=(
                                    "Your message is too long. Please shorten it and try again."
                                ))]
                            )
                        )

                    # Injection pattern check
                    for pattern in COMPILED_PATTERNS:
                        if pattern.search(user_text):
                            return LlmResponse(
                                content=types.Content(
                                    role="model",
                                    parts=[types.Part(text=(
                                        "I can only help with Acme Retail customer support. "
                                        "How can I assist you with your order today?"
                                    ))]
                                )
                            )

    # Return None to allow the model call to proceed
    return None
