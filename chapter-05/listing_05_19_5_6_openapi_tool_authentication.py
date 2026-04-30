#!/usr/bin/env python3
"""
5.6 OpenAPI Tool Authentication
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.cloud import secretmanager


def build_api_toolset(spec_str: str, spec_type: str = "yaml") -> OpenAPIToolset:
    api_key = access_secret(
        "projects/my-project/secrets/EXTERNAL_API_KEY/versions/latest"
    )
    auth_scheme, auth_credential = token_to_scheme_credential(
        "apikey", "header", "X-API-Key", api_key
    )
    return OpenAPIToolset(
        spec_str=spec_str,
        spec_str_type=spec_type,
        auth_scheme=auth_scheme,
        auth_credential=auth_credential,
    )
