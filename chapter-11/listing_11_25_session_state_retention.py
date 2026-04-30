#!/usr/bin/env python3
"""
Session State Retention
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.sessions import VertexAiSessionService

async def delete_user_sessions(
    user_id: str,
    session_service: VertexAiSessionService,
    app_name: str,
) -> dict:
    sessions = await session_service.list_sessions(
        app_name=app_name,
        user_id=user_id
    )

    deleted_count = 0
    for session in sessions.sessions:
        await session_service.delete_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session.id
        )
        deleted_count += 1

    return {
        "user_id": user_id,
        "deleted_session_count": deleted_count,
        "status": "complete"
    }
