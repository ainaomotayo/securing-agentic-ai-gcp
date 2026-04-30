#!/usr/bin/env python3
"""
GkeCodeExecutor
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents import LlmAgent
from google.adk.code_executors import GkeCodeExecutor

# Production configuration: job mode with resource limits
gke_executor = GkeCodeExecutor(
    namespace="agent-code-execution",
    executor_type="job",
    timeout_seconds=120,
    cpu_limit="500m",
    mem_limit="512Mi",
    cpu_requested="200m",
    mem_requested="256Mi",
)

gke_agent = LlmAgent(
    name="data_analysis_agent",
    model="gemini-flash-latest",
    instruction="Analyze data by writing and executing Python code.",
    code_executor=gke_executor,
)
