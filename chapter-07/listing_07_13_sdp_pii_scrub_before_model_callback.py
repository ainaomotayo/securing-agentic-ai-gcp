# Securing Agentic AI on Google Cloud
# Chapter 7 — Secure Single-Agent Architecture
# Listing: SDP fail-closed pii_scrub_before_model callback
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp

import os
import logging
from typing import Optional
import google.cloud.dlp_v2 as dlp_v2
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

logger = logging.getLogger(__name__)

# infoTypes tuned to the customer support domain.
# Full reference: docs.cloud.google.com/sensitive-data-protection/docs/infotypes-reference
# IAM required: roles/dlp.user on the agent service account.
_CS_INFOTYPES = [
    {"name": "EMAIL_ADDRESS"},
    {"name": "PHONE_NUMBER"},
    {"name": "US_SOCIAL_SECURITY_NUMBER"},
    {"name": "CREDIT_CARD_NUMBER"},
    {"name": "STREET_ADDRESS"},
]

_dlp_client: dlp_v2.DlpServiceClient | None = None


def _get_dlp_client() -> dlp_v2.DlpServiceClient:
    global _dlp_client
    if _dlp_client is None:
        _dlp_client = dlp_v2.DlpServiceClient()
    return _dlp_client


def _sdp_deidentify(text: str) -> str | None:
    """
    Replace each matched infoType value with its type token, e.g. [EMAIL_ADDRESS].
    Returns None on any failure. Callers must treat None as a hard block, not a pass.
    """
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    try:
        response = _get_dlp_client().deidentify_content(
            request={
                "parent": parent,
                "deidentify_config": {
                    "info_type_transformations": {
                        "transformations": [
                            {"primitive_transformation": {"replace_with_info_type_config": {}}}
                        ]
                    }
                },
                "inspect_config": {"info_types": _CS_INFOTYPES},
                "item": {"value": text},
            }
        )
        return response.item.value
    except Exception as exc:
        logger.error("Sensitive Data Protection unavailable: %s", exc)
        return None


def pii_scrub_before_model(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Scrub PII from model input using SDP deidentify_content. Fails closed."""
    if not llm_request.contents:
        return None
    for content in llm_request.contents:
        for part in getattr(content, "parts", []):
            if not getattr(part, "text", None):
                continue
            scrubbed = _sdp_deidentify(part.text)
            if scrubbed is None:
                logger.error(
                    "SDP unavailable; blocking request",
                    extra={"session_id": callback_context.state.get("app:session_id")},
                )
                return LlmResponse(
                    content=types.Content(
                        role="model",
                        parts=[types.Part(text=(
                            "The request cannot be processed right now. "
                            "Please try again shortly."
                        ))]
                    )
                )
            part.text = scrubbed
    return None
