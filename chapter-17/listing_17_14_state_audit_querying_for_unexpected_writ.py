#!/usr/bin/env python3
"""
State Audit: Querying for Unexpected Writes
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import asyncio
from google.adk.sessions import DatabaseSessionService

async def audit_state_writes(
    session_service: DatabaseSessionService,
    app_name: str,
    incident_start: float,
    incident_end: float,
) -> list[dict]:
    """Find all state key writes during the incident window."""
    suspicious_writes = []

    # DatabaseSessionService stores sessions; query the event history
    # for state_delta entries during the incident window
    async with session_service._get_session_conn() as conn:
        rows = await conn.fetch("""
            SELECT s.user_id, s.id as session_id, e.timestamp,
                   e.author, e.state_delta
            FROM sessions s
            JOIN session_events e ON e.session_id = s.id
            WHERE s.app_name = $1
              AND e.timestamp BETWEEN $2 AND $3
              AND e.state_delta IS NOT NULL
              AND e.state_delta != '{}'
        """, app_name, incident_start, incident_end)

        for row in rows:
            state_delta = json.loads(row["state_delta"])
            # Flag writes to app: keys by non-user authors
            for key in state_delta:
                if key.startswith("app:") and row["author"] != "user":
                    suspicious_writes.append({
                        "session_id": row["session_id"],
                        "user_id": row["user_id"],
                        "timestamp": row["timestamp"],
                        "author": row["author"],
                        "key": key,
                        "value": state_delta[key],
                    })

    return suspicious_writes
