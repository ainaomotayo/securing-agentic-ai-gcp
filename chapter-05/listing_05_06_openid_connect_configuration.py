#!/usr/bin/env python3
"""
OpenID Connect Configuration
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.auth.auth_schemes import OpenIdConnectWithConfig
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth

# Retrieve client credentials from Secret Manager
client_id = access_secret("projects/my-project/secrets/OKTA_CLIENT_ID/versions/latest")
client_secret = access_secret("projects/my-project/secrets/OKTA_CLIENT_SECRET/versions/latest")

auth_scheme = OpenIdConnectWithConfig(
    authorization_endpoint="https://your-org.okta.com/oauth2/v1/authorize",
    token_endpoint="https://your-org.okta.com/oauth2/v1/token",
    scopes=["openid", "profile", "email"]
)
auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
    oauth2=OAuth2Auth(
        client_id=client_id,
        client_secret=client_secret,
    )
)
