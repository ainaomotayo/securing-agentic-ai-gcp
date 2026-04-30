#!/usr/bin/env python3
"""
Pre-Baked Images
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

gke_executor = GkeCodeExecutor(
    namespace="agent-code-execution",
    executor_type="job",
    image="us-central1-docker.pkg.dev/your-project/agent-images/python-sandbox:2026-04-27",
    timeout_seconds=120,
    cpu_limit="500m",
    mem_limit="512Mi",
)
