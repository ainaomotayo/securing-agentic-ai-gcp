#!/usr/bin/env python3
"""
Agent-to-Agent Authentication
Chapter 16 — Secure Deployment

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

async def call_sub_agent(sub_agent_url: str, payload: dict) -> dict:
    request = google.auth.transport.requests.Request()
    token = google.oauth2.id_token.fetch_id_token(request, sub_agent_url)
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            sub_agent_url,
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            return await response.json()
