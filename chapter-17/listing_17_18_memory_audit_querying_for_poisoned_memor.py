#!/usr/bin/env python3
"""
Memory Audit: Querying for Poisoned Memories
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.memory import VertexAiMemoryBankService

async def rebuild_clean_memory(
    memory_service: VertexAiMemoryBankService,
    session_service,
    app_name: str,
    user_id: str,
    verified_before: float,  # Unix timestamp of incident start
) -> None:
    """Rebuild memory from sessions that predate the incident."""
    sessions = await session_service.list_sessions(
        app_name=app_name,
        user_id=user_id,
    )

    for session in sessions.sessions:
        if session.last_update_time < verified_before:
            await memory_service.add_session_to_memory(session)
