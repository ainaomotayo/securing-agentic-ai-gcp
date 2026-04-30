#!/usr/bin/env python3
"""
8.9 Model Armor Integration
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.cloud import modelarmor_v1  # Model Armor Python client
from google.adk.agents import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ModelArmorGuard:
    """
    Integrates Google Cloud Model Armor into ADK via callbacks.
    Screens both model inputs and outputs.
    """

    def __init__(
        self,
        project_id: str,
        location: str,
        template_name: str,
    ):
        self.client = modelarmor_v1.ModelArmorClient()
        self.template_path = (
            f"projects/{project_id}/locations/{location}/"
            f"templates/{template_name}"
        )

    def before_model(
        self,
        callback_context: CallbackContext,
        llm_request: LlmRequest,
    ) -> Optional[LlmResponse]:
        """Screen model input through Model Armor before the LLM call."""
        user_text = self._extract_last_user_message(llm_request)
        if not user_text:
            return None

        response = self.client.sanitize_user_prompt(
            request=modelarmor_v1.SanitizeUserPromptRequest(
                name=self.template_path,
                user_prompt_data=modelarmor_v1.DataItem(text=user_text),
            )
        )

        action = response.sanitization_result.filter_match_state
        if action == modelarmor_v1.FilterMatchState.MATCH_FOUND:
            logger.warning(
                "Model Armor blocked input",
                extra={
                    "session_id": callback_context.invocation_context.session.id,
                    "filter_results": str(response.sanitization_result.filter_results),
                }
            )
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=(
                        "I cannot process this request. "
                        "Please contact support if you believe this is an error."
                    ))]
                )
            )

        return None  # Input is clean: allow the model call

    def after_model(
        self,
        callback_context: CallbackContext,
        llm_response: LlmResponse,
    ) -> Optional[LlmResponse]:
        """Screen model output through Model Armor before returning to caller."""
        if not llm_response.content or not llm_response.content.parts:
            return None

        output_text = " ".join(
            p.text for p in llm_response.content.parts
            if hasattr(p, "text") and p.text
        )
        if not output_text:
            return None

        response = self.client.sanitize_model_response(
            request=modelarmor_v1.SanitizeModelResponseRequest(
                name=self.template_path,
                model_response_data=modelarmor_v1.DataItem(text=output_text),
            )
        )

        action = response.sanitization_result.filter_match_state
        if action == modelarmor_v1.FilterMatchState.MATCH_FOUND:
            logger.warning(
                "Model Armor blocked output",
                extra={"session_id": callback_context.invocation_context.session.id}
            )
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=(
                        "I cannot provide this response. Please rephrase your request."
                    ))]
                )
            )

        return None

    def _extract_last_user_message(self, llm_request: LlmRequest) -> Optional[str]:
        if not llm_request.contents:
            return None
        last = llm_request.contents[-1]
        for part in getattr(last, "parts", []):
            if hasattr(part, "text") and part.text:
                return part.text
        return None
