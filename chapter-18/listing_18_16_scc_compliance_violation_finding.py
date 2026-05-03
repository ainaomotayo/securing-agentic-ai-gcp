# Securing Agentic AI on Google Cloud
# Chapter 18 — Governance, Compliance, and the Regulatory Landscape
# Listing: SCC finding for GDPR Article 22 compliance violations
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# Add to the compliance plugin module and call from compliance_before_tool_callback.
# IAM required: roles/securitycenter.findingsEditor on the SCC source.
# Environment variables: GOOGLE_CLOUD_ORGANIZATION_ID, COMPLIANCE_SCC_SOURCE_ID

import logging
import os
import time
import uuid
from google.cloud import securitycenter_v2

_compliance_scc_client: securitycenter_v2.SecurityCenterClient | None = None


def _get_compliance_scc_client() -> securitycenter_v2.SecurityCenterClient:
    global _compliance_scc_client
    if _compliance_scc_client is None:
        _compliance_scc_client = securitycenter_v2.SecurityCenterClient()
    return _compliance_scc_client


def _create_compliance_violation_finding(
    tool_name: str,
    invocation_id: str,
    violation_type: str,
    regulation: str,
) -> None:
    """
    Creates an SCC finding for a critical compliance violation.
    Reads organization_id and source_id from environment variables.
    Fails silently: the Cloud Logging record already exists as the authoritative
    audit trail. The SCC finding is a secondary escalation surface.
    IAM role required: roles/securitycenter.findingsEditor.
    """
    organization_id = os.environ.get("GOOGLE_CLOUD_ORGANIZATION_ID", "")
    source_id = os.environ.get("COMPLIANCE_SCC_SOURCE_ID", "")
    if not organization_id or not source_id:
        return

    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    finding_id = uuid.uuid4().hex
    parent = f"organizations/{organization_id}/sources/{source_id}/locations/global"
    finding = securitycenter_v2.Finding(
        state=securitycenter_v2.Finding.State.ACTIVE,
        severity=securitycenter_v2.Finding.Severity.CRITICAL,
        category=violation_type,
        description=(
            f"Agent attempted to invoke '{tool_name}' without required human confirmation. "
            f"Regulation: {regulation}. Tool call blocked."
        ),
        event_time={"seconds": int(time.time())},
        resource_name=f"//run.googleapis.com/projects/{project_id}",
    )
    try:
        _get_compliance_scc_client().create_finding(
            request=securitycenter_v2.CreateFindingRequest(
                parent=parent,
                finding_id=finding_id,
                finding=finding,
            )
        )
    except Exception as exc:
        logging.getLogger("compliance").warning(
            "SCC finding creation failed (non-blocking): %s", exc
        )


# Usage in compliance_before_tool_callback (Article 22 violation path):
#
#     if tool.name in ARTICLE_22_TOOLS:
#         hitl_record = tool_context.state.get(f"temp:hitl_confirmed_{tool.name}", False)
#         if not hitl_record:
#             logging.getLogger("compliance").error(json.dumps({
#                 "event_type": "gdpr_art22_violation_attempt",
#                 "tool_name": tool.name,
#                 "invocation_id": tool_context.invocation_id,
#                 "compliance": ["gdpr_art22", "eu_ai_act_art14", "korea_aiba"],
#             }))
#             _create_compliance_violation_finding(
#                 tool_name=tool.name,
#                 invocation_id=tool_context.invocation_id,
#                 violation_type="GDPR_ARTICLE_22_VIOLATION",
#                 regulation="GDPR Article 22 / EU AI Act Article 14 / Korea AI Basic Act",
#             )
#             return {"error": f"Tool {tool.name} requires human review before execution."}
