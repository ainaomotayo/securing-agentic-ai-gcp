# Securing Agentic AI on Google Cloud
# Chapter 17 — Incident Response
# Listing: SDP pseudonymization for monitoring data (GDPR Article 5(1)(b))
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# Pseudonymizes tool args before writing to Cloud Logging / SCC / Cloud Monitoring.
# Do NOT pseudonymize forensic archive data. See listing_17_24 for the raw archive pattern.
# IAM required: roles/dlp.user on the agent service account.

import json
import logging
import os
import google.cloud.dlp_v2 as dlp_v2

logger = logging.getLogger(__name__)

_dlp_client = dlp_v2.DlpServiceClient()

_ARG_INFOTYPES = [
    {"name": "EMAIL_ADDRESS"},
    {"name": "PHONE_NUMBER"},
    {"name": "US_SOCIAL_SECURITY_NUMBER"},
    {"name": "CREDIT_CARD_NUMBER"},
    {"name": "FINANCIAL_ACCOUNT_NUMBER"},
    {"name": "STREET_ADDRESS"},
]


def _pseudonymize_for_monitoring(data: dict) -> dict:
    """
    Pseudonymize string values in a dict before writing to Cloud Logging, SCC,
    or Cloud Monitoring. Replaces each matched infoType value with its token,
    e.g. customer@example.com becomes [EMAIL_ADDRESS].
    Returns {"_sdp_unavailable": True} if SDP is unreachable, omitting args entirely
    to prevent PII leakage into monitoring streams.

    PII in monitoring streams violates GDPR Article 5(1)(b) (purpose limitation):
    the data was collected for the agent task, not for security team review.
    """
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    text = json.dumps(data)
    try:
        response = _dlp_client.deidentify_content(
            request={
                "parent": parent,
                "deidentify_config": {
                    "info_type_transformations": {
                        "transformations": [
                            {"primitive_transformation": {"replace_with_info_type_config": {}}}
                        ]
                    }
                },
                "inspect_config": {"info_types": _ARG_INFOTYPES},
                "item": {"value": text},
            }
        )
        return json.loads(response.item.value)
    except Exception as exc:
        logger.warning(
            "SDP pseudonymization unavailable for monitoring data: %s. "
            "Tool args omitted from log entry to prevent PII leakage.", exc
        )
        return {"_sdp_unavailable": True}
