#!/usr/bin/env python3
"""
In-memory approval store (use a persistent queue in production)
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import LlmAgent
from google.adk.code_executors import GkeCodeExecutor

gke_executor = GkeCodeExecutor(
    namespace="agent-code-execution",
    executor_type="job",
    timeout_seconds=120,
    cpu_limit="500m",
    mem_limit="512Mi",
)

data_analysis_agent = LlmAgent(
    name="data_analysis_agent",
    model="gemini-flash-latest",
    instruction="Analyze the provided data file and answer the user's question.",
    code_executor=gke_executor,
    before_tool_callback=code_execution_hitl_gate,
)
