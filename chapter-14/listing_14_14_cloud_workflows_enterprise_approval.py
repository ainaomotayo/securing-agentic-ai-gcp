# Securing Agentic AI on Google Cloud
# Chapter 14 — Human-in-the-Loop Security Controls
# Listing: Cloud Workflows enterprise approval gate (before_tool_callback)
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# IAM required: roles/workflows.invoker on the agent service account.
# Deploy wire-transfer-approval.yaml to Cloud Workflows before use.

import functools
import json
import logging
import os
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.cloud.workflows import executions_v1

logger = logging.getLogger(__name__)
_approval_executions_client = executions_v1.ExecutionsClient()


def _start_approval_workflow(
    project_id: str,
    location: str,
    workflow_id: str,
    payload: dict,
) -> str:
    """Trigger an approval workflow execution. Returns the execution resource name."""
    parent = f"projects/{project_id}/locations/{location}/workflows/{workflow_id}"
    execution = executions_v1.Execution(argument=json.dumps(payload))
    response = _approval_executions_client.create_execution(
        parent=parent,
        execution=execution,
    )
    return response.name


def _poll_approval_decision(execution_name: str) -> Optional[dict]:
    """Return the decision dict when the execution completes; None if still running."""
    execution = _approval_executions_client.get_execution(name=execution_name)
    if execution.state == executions_v1.Execution.State.SUCCEEDED:
        return json.loads(execution.result)
    if execution.state in (
        executions_v1.Execution.State.FAILED,
        executions_v1.Execution.State.CANCELLED,
    ):
        return {"approved": False, "reason": "Approval workflow failed or was cancelled."}
    return None  # ACTIVE or QUEUED: still waiting


def enterprise_approval_hitl_gate(
    tool: BaseTool,
    args: dict,
    tool_context: ToolContext,
    project_id: str,
    location: str,
    workflow_id: str,
) -> Optional[dict]:
    """
    before_tool_callback: route high-value transfers through Cloud Workflows approval.
    Stores the execution name in session state so retries within the same invocation
    poll the existing execution rather than creating a new one.
    IAM required: roles/workflows.invoker on the agent service account.
    """
    APPROVAL_TOOLS = {"initiate_wire_transfer", "approve_payment_batch"}
    if tool.name not in APPROVAL_TOOLS:
        return None

    invocation_id = tool_context.invocation_id
    exec_key = f"temp:approval_execution:{invocation_id}:{tool.name}"

    execution_name = tool_context.state.get(exec_key)
    if not execution_name:
        payload = {
            "invocation_id": invocation_id,
            "session_id": tool_context.session.id,
            "tool_name": tool.name,
            "amount_usd": args.get("amount_usd", 0),
            "vendor_name": args.get("vendor_name", "unknown"),
        }
        execution_name = _start_approval_workflow(
            project_id, location, workflow_id, payload
        )
        tool_context.state[exec_key] = execution_name
        logger.info(
            "Enterprise approval workflow started",
            extra={"execution": execution_name, "invocation_id": invocation_id},
        )

    decision = _poll_approval_decision(execution_name)

    if decision is None:
        return {
            "status": "pending_approval",
            "message": (
                "Approval request sent. The approver will receive a Cloud Workflows "
                "callback URL and must respond before this transfer can proceed."
            ),
        }

    tool_context.state.pop(exec_key, None)

    if decision.get("approved"):
        logger.info(
            "Transfer approved via Cloud Workflows",
            extra={"invocation_id": invocation_id, "tool": tool.name},
        )
        return None

    return {
        "status": "rejected",
        "reason": decision.get("reason", "Rejected by approver."),
    }


# Wire with functools.partial at agent initialization:
#
# payment_agent = LlmAgent(
#     name="payment_agent",
#     model="gemini-2.0-flash-001",
#     instruction="Process vendor payments. All wire transfers require approval.",
#     tools=[initiate_wire_transfer, approve_payment_batch],
#     before_tool_callback=functools.partial(
#         enterprise_approval_hitl_gate,
#         project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
#         location="us-central1",
#         workflow_id="wire-transfer-approval",
#     ),
# )
