#!/usr/bin/env python3
"""
AgentEngineSandboxCodeExecutor
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.agents.llm_agent import Agent
from google.adk.code_executors.agent_engine_sandbox_code_executor import AgentEngineSandboxCodeExecutor

root_agent = Agent(
    model="gemini-flash-latest",
    name="data_analysis_agent",
    instruction="""
    You are a data analysis assistant.
    You SHOULD NEVER install any package on your own like `pip install ...`.
    All code snippets will be executed within the sandbox environment.
    """,
    code_executor=AgentEngineSandboxCodeExecutor(
        sandbox_resource_name="SANDBOX_RESOURCE_NAME",
    ),
)
