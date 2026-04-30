#!/usr/bin/env python3
"""
7.8 Hardening Step 7: RunConfig Safety Settings
Chapter 07 — Secure Single Agent Architecture

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.runners import RunConfig

run_config = RunConfig(
    max_llm_calls=10,        # Maximum model calls per invocation (default: unlimited)
    response_modalities=["TEXT"],  # Restrict output types to text only
)

# Pass to the runner when invoking the agent
# runner.run(user_message, run_config=run_config)
