# Securing Agentic AI on Google Cloud
# Chapter 10 — Tool Security
# Listing: SDP-backed after_tool_callback for PII scrubbing on tool outputs
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# IAM required: roles/dlp.user on the agent service account.

import json
import logging
import os
from typing import Any, Dict, Optional

import google.cloud.dlp_v2 as dlp_v2
from google.adk.agents import LlmAgent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

# Tools whose results may contain customer or personal data.
# Extend this set as new data-bearing tools are added to the agent.
SENSITIVE_TOOLS = {
    "get_customer_profile",
    "query_order_history",
    "fetch_billing_record",
    "search_user_accounts",
}

_OUTPUT_INFOTYPES = [
    {"name": "EMAIL_ADDRESS"},
    {"name": "PHONE_NUMBER"},
    {"name": "US_SOCIAL_SECURITY_NUMBER"},
    {"name": "CREDIT_CARD_NUMBER"},
    {"name": "STREET_ADDRESS"},
    {"name": "FINANCIAL_ACCOUNT_NUMBER"},
]

_tool_dlp_client: dlp_v2.DlpServiceClient | None = None


def _get_tool_dlp_client() -> dlp_v2.DlpServiceClient:
    global _tool_dlp_client
    if _tool_dlp_client is None:
        _tool_dlp_client = dlp_v2.DlpServiceClient()
    return _tool_dlp_client


def _sdp_deidentify_text(text: str) -> str | None:
    """
    Replace matched infoType values with type tokens, e.g. [EMAIL_ADDRESS].
    Returns None on any failure. Callers must treat None as a hard block.
    """
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    try:
        response = _get_tool_dlp_client().deidentify_content(
            request={
                "parent": parent,
                "deidentify_config": {
                    "info_type_transformations": {
                        "transformations": [
                            {"primitive_transformation": {"replace_with_info_type_config": {}}}
                        ]
                    }
                },
                "inspect_config": {"info_types": _OUTPUT_INFOTYPES},
                "item": {"value": text},
            }
        )
        return response.item.value
    except Exception as exc:
        logger.error("SDP deidentify_content failed on tool output: %s", exc)
        return None


def sanitize_tool_output(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Dict,
) -> Optional[Dict]:
    """
    Scrub PII from tool outputs for data-bearing tools. Fails closed:
    if SDP is unreachable, returns an error result rather than forwarding
    unscreened data to the model.
    IAM required: roles/dlp.user on the agent service account.
    """
    if tool.name not in SENSITIVE_TOOLS:
        return None

    response_text = json.dumps(tool_response)
    scrubbed_text = _sdp_deidentify_text(response_text)

    if scrubbed_text is None:
        logger.error(
            "SDP unavailable; blocking tool output",
            extra={"tool": tool.name, "session_id": tool_context.session.id},
        )
        return {"error": f"The result from {tool.name} could not be screened. Please try again."}

    try:
        return json.loads(scrubbed_text)
    except json.JSONDecodeError:
        return {"result": scrubbed_text}
