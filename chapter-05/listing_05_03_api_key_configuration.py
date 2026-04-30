#!/usr/bin/env python3
"""
API Key Configuration
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

# Retrieve key from Secret Manager, not hardcoded
api_key = access_secret("projects/my-project/secrets/WEATHER_API_KEY/versions/latest")

auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey", "header", "X-API-Key", api_key
)
weather_toolset = OpenAPIToolset(
    spec_str=weather_openapi_spec_str,
    spec_str_type="yaml",
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
