#!/usr/bin/env python3
"""
Read-Time Memory Validation
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import ToolContext
from google.adk.memory import VertexAiMemoryBankService

async def screened_load_memory(
    query: str,
    tool_context: ToolContext,
) -> dict:
    """Load memories and screen them for adversarial content before returning."""
    results = await tool_context.invocation_context.memory_service.search_memory(
        app_name=tool_context.invocation_context.session.app_name,
        user_id=tool_context.invocation_context.session.user_id,
        query=query
    )

    safe_memories = []
    flagged_count = 0

    for memory in results.memories:
        content_text = str(memory.content) if memory.content else ""
        if _contains_injection_attempt(content_text):
            flagged_count += 1
            continue  # Drop the poisoned memory; do not return it to the model
        safe_memories.append({"content": content_text})

    if flagged_count > 0:
        import logging
        logging.warning(
            "Dropped %d flagged memories from query '%s'",
            flagged_count,
            query,
        )

    return {"memories": safe_memories, "count": len(safe_memories)}
