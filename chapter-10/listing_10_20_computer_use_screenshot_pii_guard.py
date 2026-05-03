# Securing Agentic AI on Google Cloud
# Chapter 10 — Tool Security
# Listing: SDP-backed after_tool_callback for Computer Use screenshot PII guard
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# IAM required: roles/dlp.user on the agent service account.

import base64
import logging
import os
from typing import Any, Dict, Optional

import google.cloud.dlp_v2 as dlp_v2
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

_SCREENSHOT_INFOTYPES = [
    {"name": "EMAIL_ADDRESS"},
    {"name": "PHONE_NUMBER"},
    {"name": "CREDIT_CARD_NUMBER"},
    {"name": "US_SOCIAL_SECURITY_NUMBER"},
    {"name": "FINANCIAL_ACCOUNT_NUMBER"},
]


def _inspect_screenshot_for_pii(image_b64: str) -> bool:
    """
    Returns True if SDP detects PII in the screenshot image.
    Returns True (conservative) on any API failure to prevent inadvertent logging.
    IAM required: roles/dlp.user on the agent service account.
    """
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    client = dlp_v2.DlpServiceClient()
    try:
        response = client.inspect_content(
            request={
                "parent": parent,
                "inspect_config": {
                    "info_types": _SCREENSHOT_INFOTYPES,
                    "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
                },
                "item": {
                    "byte_item": {
                        "type_": dlp_v2.ByteContentItem.BytesType.IMAGE_PNG,
                        "data": base64.b64decode(image_b64),
                    }
                },
            }
        )
        return len(response.result.findings) > 0
    except Exception as exc:
        logger.error("SDP screenshot inspection failed: %s; treating as PII-present", exc)
        return True


def computer_use_screenshot_guard(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Dict,
) -> Optional[Dict]:
    """
    after_tool_callback for Computer Use: inspect screenshots for PII and
    suppress them from Cloud Logging when PII is detected. The model still
    receives the screenshot for task completion; only the log entry is suppressed.
    """
    if tool.name != "screenshot":
        return None

    image_b64 = tool_response.get("screenshot", "")
    if not image_b64:
        return None

    if _inspect_screenshot_for_pii(image_b64):
        logger.info(
            "Screenshot suppressed from log: PII detected",
            extra={"session_id": tool_context.session.id, "tool": tool.name},
        )
        tool_context.state["temp:screenshot_pii_detected"] = True
        return tool_response

    return None
