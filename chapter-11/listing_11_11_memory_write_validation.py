#!/usr/bin/env python3
"""
Memory Write Validation
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import re
from google.adk.agents import Agent
from google import adk

# Patterns that signal attempted memory poisoning
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instruction",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"from\s+now\s+on\s+you",
    r"per\s+(established|official|company)\s+policy",
    r"always\s+(approve|grant|allow)\s+",
    r"never\s+(reject|deny|refuse)\s+",
    r"system\s+prompt\s*:",
]

def _contains_injection_attempt(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(p, text_lower) for p in INJECTION_PATTERNS)

def _extract_user_content_from_session(session) -> list[str]:
    user_texts = []
    for event in session.events:
        if event.author == "user" and event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    user_texts.append(part.text)
    return user_texts

async def validated_save_to_memory_callback(callback_context):
    session = callback_context._invocation_context.session
    user_texts = _extract_user_content_from_session(session)

    for text in user_texts:
        if _contains_injection_attempt(text):
            # Flag for security review, do not write to memory
            import logging
            logging.warning(
                "Memory poisoning attempt detected in session %s for user %s",
                session.id,
                session.user_id,
            )
            return  # Skip add_session_to_memory entirely

    # Content passed validation; proceed with memory ingestion
    await callback_context._invocation_context.memory_service.add_session_to_memory(session)
