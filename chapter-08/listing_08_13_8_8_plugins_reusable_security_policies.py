#!/usr/bin/env python3
"""
8.8 Plugins: Reusable Security Policies
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.plugins import BasePlugin
from google.adk.agents import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext
from typing import Optional, Dict, Any
import logging
import json
import hashlib
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class OrganizationSecurityPlugin(BasePlugin):
    """
    Org-wide security plugin: audit logging + PII scrubbing + rate limiting.
    Attach to the runner to apply across all agents.
    """

    def __init__(self) -> None:
        super().__init__(name="org_security_plugin")

    async def before_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_request: LlmRequest,
    ) -> Optional[LlmResponse]:
        """Log every model call and apply org-wide PII scrubbing."""
        session_id = callback_context.state.get("app:session_id", "unknown")
        logger.info(json.dumps({
            "event": "model_call",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "agent": callback_context.agent_name,
        }))
        # PII scrubbing logic here (reuse the function from Section 8.4)
        return None

    async def after_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_response: LlmResponse,
    ) -> Optional[LlmResponse]:
        """Apply org-wide PII redaction to all model responses."""
        # PII redaction logic here (reuse the function from Section 8.5)
        return None

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        args: Dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[Dict]:
        """Log all tool calls for the audit trail."""
        logger.info(json.dumps({
            "event": "tool_call",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": tool.name,
            "args_hash": hashlib.sha256(str(args).encode()).hexdigest()[:16],
            "session_id": tool_context.invocation_context.session.id,
        }))
        return None

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        args: Dict[str, Any],
        tool_context: ToolContext,
        tool_response: Dict,
    ) -> Optional[Dict]:
        """Sanitize all tool results org-wide."""
        # Injection pattern check here (reuse function from Section 8.7)
        return None
