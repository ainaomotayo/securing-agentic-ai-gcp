#!/usr/bin/env python3
"""
Resource Limits as DoS Mitigation
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

gke_executor = GkeCodeExecutor(
    namespace="agent-code-execution",
    executor_type="job",
    timeout_seconds=60,        # Hard wall clock limit
    cpu_limit="500m",          # 0.5 CPU cores maximum
    mem_limit="512Mi",         # 512MB memory maximum
    cpu_requested="200m",      # Guaranteed CPU allocation
    mem_requested="256Mi",     # Guaranteed memory allocation
)
