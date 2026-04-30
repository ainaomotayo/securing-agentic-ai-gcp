#!/usr/bin/env python3
"""
DatabaseSessionService
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.sessions import DatabaseSessionService

# SQLite requires the aiosqlite async driver
db_url = "postgresql+asyncpg://user:password@host:5432/agent_sessions"
session_service = DatabaseSessionService(db_url=db_url)
