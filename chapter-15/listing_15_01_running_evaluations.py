#!/usr/bin/env python3
"""
Running Evaluations
Chapter 15 — Evaluation Red Teaming

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

@pytest.mark.asyncio
async def test_security_eval_suite():
    """Run the complete adversarial security eval suite."""
    await AgentEvaluator.evaluate(
        agent_module="customer_support_agent",
        eval_dataset_file_path_or_dir="tests/security/adversarial_eval_set.evalset.json",
    )
