#!/usr/bin/env python3
"""
OAuth2 Configuration
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from fastapi.openapi.models import OAuth2, OAuthFlowAuthorizationCode, OAuthFlows
from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth

# Retrieve client secret from Secret Manager at startup
client_id = access_secret("projects/my-project/secrets/CALENDAR_CLIENT_ID/versions/latest")
client_secret = access_secret("projects/my-project/secrets/CALENDAR_CLIENT_SECRET/versions/latest")

auth_scheme = OAuth2(
    flows=OAuthFlows(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl="https://accounts.google.com/o/oauth2/auth",
            tokenUrl="https://oauth2.googleapis.com/token",
            scopes={
                "https://www.googleapis.com/auth/calendar": "calendar scope"
            },
        )
    )
)
auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id=client_id,
        client_secret=client_secret,
    ),
)

calendar_toolset = OpenAPIToolset(
    spec_str=google_calendar_openapi_spec_str,
    spec_str_type="yaml",
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
