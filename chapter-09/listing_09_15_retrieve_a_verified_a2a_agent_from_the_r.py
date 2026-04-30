#!/usr/bin/env python3
"""
Retrieve a verified A2A agent from the registry; identity is managed by the platform
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import httpx
import google.auth
from google.auth.transport.requests import Request

class GoogleAuth(httpx.Auth):
    def __init__(self):
        self.creds, _ = google.auth.default()
    def auth_flow(self, request):
        if not self.creds.valid:
            self.creds.refresh(Request())
        request.headers["Authorization"] = f"Bearer {self.creds.token}"
        yield request

httpx_client = httpx.AsyncClient(auth=GoogleAuth(), timeout=httpx.Timeout(60.0))
reports_agent = registry.get_remote_a2a_agent(
    agent_name=agent_name,
    httpx_client=httpx_client,
)
