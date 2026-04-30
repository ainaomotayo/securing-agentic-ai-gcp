#!/usr/bin/env python3
"""
10.7 OAuth for User-Delegated Tool Access
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.tools import AuthCredential, OAuth2, AuthScheme
from google.adk.tools.openapi_tool.auth.auth_credential import OAuth2Auth

# Tool configured for three-legged OAuth (user-delegated access)
calendar_toolset = OpenAPIToolset(
    spec_url="https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest",
    auth_scheme=OAuth2(
        flows=OAuth2Auth(
            authorization_url="https://accounts.google.com/o/oauth2/auth",
            token_url="https://oauth2.googleapis.com/token",
            scopes={
                # Minimum scope: read-only calendar access
                # Do NOT use: https://www.googleapis.com/auth/calendar (full access)
                "https://www.googleapis.com/auth/calendar.readonly": "Read calendar events",
            },
        )
    ),
    auth_credential=AuthCredential(
        auth_type="OAUTH2",
        oauth2=OAuth2Auth(
            client_id=get_secret("google-oauth-client-id"),
            client_secret=get_secret("google-oauth-client-secret"),
        ),
    ),
)
