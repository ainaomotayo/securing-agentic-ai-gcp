#!/usr/bin/env python3
"""
5.1 ADK Authentication Primitives: AuthScheme and AuthCredential
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

sample_api_toolset = OpenAPIToolset(
    spec_str=openapi_spec_str,
    spec_str_type="yaml",
    auth_scheme=auth_scheme,       # how the API authenticates
    auth_credential=auth_credential,  # what credentials start the flow
)
