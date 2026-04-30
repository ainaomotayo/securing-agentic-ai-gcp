#!/usr/bin/env python3
"""
State Audit: Querying for Unexpected Writes
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

async def reset_app_state_key(
    session_service: DatabaseSessionService,
    app_name: str,
    key: str,
    safe_value: any,
) -> None:
    """Reset an app: state key to a known-safe value across all sessions."""
    async with session_service._get_session_conn() as conn:
        await conn.execute("""
            UPDATE sessions
            SET app_state = jsonb_set(app_state, $1, $2::jsonb)
            WHERE app_name = $3
        """, "{" + key.replace("app:", "") + "}", json.dumps(safe_value), app_name)
