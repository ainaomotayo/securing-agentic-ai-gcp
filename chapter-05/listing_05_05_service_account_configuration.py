#!/usr/bin/env python3
"""
Service Account Configuration
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.openapi_tool.auth.auth_helpers import service_account_dict_to_scheme_credential
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
import json

# Retrieve JSON key from Secret Manager, not from disk
sa_json_str = access_secret("projects/my-project/secrets/AGENT_SA_KEY/versions/latest")
service_account_cred = json.loads(sa_json_str)

auth_scheme, auth_credential = service_account_dict_to_scheme_credential(
    config=service_account_cred,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
sample_toolset = OpenAPIToolset(
    spec_str=sa_openapi_spec_str,
    spec_str_type="json",
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
