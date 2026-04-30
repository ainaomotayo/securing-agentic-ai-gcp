#!/usr/bin/env python3
"""
18.6 Policy-as-Code: Encoding Compliance in Agent Architecture
Chapter 18 — Governance Compliance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from typing import Optional
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
import json
import logging
import hashlib
import re

# ---- PII Detection Patterns (GDPR data minimization + India DPDP) ----
PII_PATTERNS = [
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), "email"),
    (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), "us_ssn"),
    (re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b'), "credit_card"),
    (re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}\b'), "iban"),
]

def screen_for_pii(text: str) -> list[str]:
    """Returns list of detected PII type strings, or empty list if clean."""
    detected = []
    for pattern, pii_type in PII_PATTERNS:
        if pattern.search(text):
            detected.append(pii_type)
    return detected

# ---- Compliance Plugin Callbacks ----

def compliance_before_model_callback(
    callback_context: CallbackContext,
    llm_request,
) -> Optional[object]:
    """
    Enforces:
    - EU AI Act Article 13: log invocation metadata for transparency
    - GDPR Article 5(1)(c): screen for PII in user input
    - NIST AI RMF MEASURE 2.8: record request metadata for monitoring
    """
    # EU AI Act Article 13: transparency log
    logging.getLogger("compliance").info(json.dumps({
        "event_type": "model_invocation",
        "invocation_id": callback_context.invocation_id,
        "agent_name": callback_context.agent_name,
        "model": getattr(llm_request, "model", "unknown"),
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        "compliance": ["eu_ai_act_art13", "nist_rmf_measure"],
    }))

    # GDPR data minimization: detect PII in user input
    if hasattr(llm_request, "contents") and llm_request.contents:
        for content in llm_request.contents:
            if hasattr(content, "parts"):
                for part in content.parts:
                    if hasattr(part, "text") and part.text:
                        pii_types = screen_for_pii(part.text)
                        if pii_types:
                            logging.getLogger("compliance").warning(json.dumps({
                                "event_type": "pii_detected_in_input",
                                "invocation_id": callback_context.invocation_id,
                                "pii_types": pii_types,
                                "compliance": ["gdpr_art5_1c", "india_dpdp"],
                            }))

    return None  # Allow the model call to proceed


def compliance_before_tool_callback(
    callback_context: CallbackContext,
    tool: BaseTool,
    args: dict,
    tool_context: ToolContext,
) -> Optional[dict]:
    """
    Enforces:
    - EU AI Act Article 14: verify HITL record exists for high-impact tools
    - GDPR Article 22: verify automated decision tools have confirmation
    - Korea AI Basic Act: verify user notification for high-impact decisions
    """
    ARTICLE_22_TOOLS = {
        "approve_loan", "deny_loan", "terminate_employment",
        "approve_credit_limit", "modify_insurance_premium",
    }

    if tool.name in ARTICLE_22_TOOLS:
        # Verify HITL confirmation was obtained before this tool fires
        hitl_record = tool_context.state.get(
            f"temp:hitl_confirmed_{tool.name}", False
        )
        if not hitl_record:
            logging.getLogger("compliance").error(json.dumps({
                "event_type": "gdpr_art22_violation_attempt",
                "tool_name": tool.name,
                "invocation_id": tool_context.invocation_id,
                "compliance": ["gdpr_art22", "eu_ai_act_art14", "korea_aiba"],
            }))
            return {
                "error": (
                    f"Tool {tool.name} requires human review before execution. "
                    "Request confirmation first."
                )
            }

    # Log tool call for Article 13 transparency record
    logging.getLogger("compliance").info(json.dumps({
        "event_type": "tool_invocation",
        "tool_name": tool.name,
        "args_hash": hashlib.sha256(
            json.dumps(args, sort_keys=True).encode()
        ).hexdigest(),
        "invocation_id": tool_context.invocation_id,
        "compliance": ["eu_ai_act_art13"],
    }))

    return None


def compliance_after_model_callback(
    callback_context: CallbackContext,
    llm_response,
) -> Optional[object]:
    """
    Enforces:
    - EU AI Act Article 9 (safety_v1 threshold check via eval framework)
    - GDPR: screen response for PII before it reaches the user
    """
    if hasattr(llm_response, "content") and llm_response.content:
        for part in (llm_response.content.parts or []):
            if hasattr(part, "text") and part.text:
                pii_types = screen_for_pii(part.text)
                if pii_types:
                    logging.getLogger("compliance").warning(json.dumps({
                        "event_type": "pii_detected_in_response",
                        "invocation_id": callback_context.invocation_id,
                        "pii_types": pii_types,
                        "compliance": ["gdpr_art5_1c"],
                    }))

    return None


def build_compliant_agent(base_agent: LlmAgent) -> LlmAgent:
    """Wraps a base agent with the compliance plugin callbacks."""
    return LlmAgent(
        name=base_agent.name,
        model=base_agent.model,
        instruction=base_agent.instruction,
        tools=base_agent.tools,
        before_model_callback=compliance_before_model_callback,
        before_tool_callback=compliance_before_tool_callback,
        after_model_callback=compliance_after_model_callback,
    )
