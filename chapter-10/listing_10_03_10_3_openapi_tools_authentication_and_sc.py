#!/usr/bin/env python3
"""
10.3 OpenAPI Tools: Authentication and Schema Validation
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import service_account_dict_to_scheme_credential
from google.adk.tools import AuthScheme, AuthCredential, APIKey
from google.cloud import secretmanager
import json

def get_api_key_from_secret_manager(secret_name: str) -> str:
    """Retrieve API key from Secret Manager. Never hardcode credentials."""
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode("UTF-8")

# Retrieve credential from Secret Manager, not from environment variable
api_key = get_api_key_from_secret_manager(
    "projects/my-project/secrets/external-api-key/versions/latest"
)

external_api_toolset = OpenAPIToolset(
    spec_url="https://api.example.com/openapi.json",
    auth_scheme=APIKey(name="X-API-Key", location="header"),
    auth_credential=AuthCredential(
        auth_type="API_KEY",
        api_key=api_key,
    ),
)
