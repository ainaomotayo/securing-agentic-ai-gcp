#!/usr/bin/env python3
"""
Opening Scenario: The Prototype That Became Production
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id="987654321-abc.apps.googleusercontent.com",
        client_secret="GOCSPX-abcdefghijklmnop12345678",
    ),
)
