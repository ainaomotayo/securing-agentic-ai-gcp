#!/usr/bin/env python3
"""
8.8 Plugins: Reusable Security Policies
Chapter 08 — Guardrails Callbacks Model Armor

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.runners import Runner

security_plugin = OrganizationSecurityPlugin()

runner = Runner(
    agent=root_agent,
    session_service=session_service,
    plugins=[security_plugin],  # Applied to every agent in this runner
)
