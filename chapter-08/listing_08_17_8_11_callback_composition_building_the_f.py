#!/usr/bin/env python3
"""
8.11 Callback Composition: Building the Full Stack
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from typing import Optional, Callable
from google.adk.agents import CallbackContext
from google.adk.models import LlmRequest, LlmResponse


def compose_before_model(
    *callbacks: Callable,
) -> Callable:
    """
    Compose multiple before_model callbacks into a single function.
    Returns the first blocking response; proceeds if all return None.
    """
    def composed(
        callback_context: CallbackContext,
        llm_request: LlmRequest,
    ) -> Optional[LlmResponse]:
        for cb in callbacks:
            result = cb(callback_context, llm_request)
            if result is not None:
                return result  # Short-circuit: first block wins
        return None

    return composed


# Application: compose cheap regex check + Model Armor + domain safety judge
model_armor = ModelArmorGuard(
    project_id="my-project",
    location="us-central1",
    template_name="legal-services-baseline",
)
safety_judge = GeminiSafetyJudge()

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="legal_support_agent",
    instruction=SYSTEM_INSTRUCTION,
    tools=[...],
    before_model_callback=compose_before_model(
        pii_scrub_before_model,           # Fast: regex, no external call
        model_armor.before_model,         # Medium: Model Armor API call
        safety_judge.before_model,        # Slowest: secondary model call
    ),
    after_model_callback=compose_after_model(
        pii_redact_after_model,           # Fast: regex
        model_armor.after_model,          # Model Armor output check
    ),
)
