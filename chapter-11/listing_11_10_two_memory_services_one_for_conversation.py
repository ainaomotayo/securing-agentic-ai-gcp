#!/usr/bin/env python3
"""
Two memory services: one for conversation history, one for authoritative policy
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import ToolContext

async def retrieve_with_source_labels(
    query: str,
    tool_context: ToolContext,
) -> dict:
    conversation_results = await conversation_memory.search_memory(
        app_name=APP_NAME,
        user_id=tool_context.session.user_id,
        query=query
    )
    policy_results = await policy_memory.search_memory(
        app_name=APP_NAME,
        user_id="__system__",
        query=query
    )

    return {
        "conversation_context": [
            {"source": "user_history", "content": m.content}
            for m in conversation_results.memories
        ],
        "policy_context": [
            {"source": "authoritative_policy", "content": m.content}
            for m in policy_results.memories
        ]
    }
