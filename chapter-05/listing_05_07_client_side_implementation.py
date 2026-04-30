#!/usr/bin/env python3
"""
Client-Side Implementation
Chapter 05 — Authentication Patterns

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.auth import AuthConfig
from google.adk.events import Event
from google.genai import types


def get_auth_request_function_call(event: Event) -> types.FunctionCall | None:
    if not event.content or not event.content.parts:
        return None
    for part in event.content.parts:
        if (
            part
            and part.function_call
            and part.function_call.name == "adk_request_credential"
            and event.long_running_tool_ids
            and part.function_call.id in event.long_running_tool_ids
        ):
            return part.function_call
    return None


async def run_with_oauth(runner, session, content):
    # First run: detect auth request
    auth_function_call_id = None
    auth_config = None

    async for event in runner.run_async(
        session_id=session.id, user_id="user", new_message=content
    ):
        if (fc := get_auth_request_function_call(event)):
            auth_function_call_id = fc.id
            auth_config = AuthConfig.model_validate(fc.args.get("authConfig"))
            break

    if not auth_function_call_id:
        return  # no auth required

    # Redirect user to authorization URL
    redirect_uri = "https://your-app.example.com/oauth/callback"
    auth_url = auth_config.exchanged_auth_credential.oauth2.auth_uri
    full_auth_url = f"{auth_url}&redirect_uri={redirect_uri}"

    # (In a web app, redirect the user's browser to full_auth_url)
    # (In a CLI, print the URL and prompt the user to paste back the callback URL)
    auth_response_uri = await prompt_user_for_callback_url(full_auth_url)

    # Submit callback URL back to ADK
    auth_config.exchanged_auth_credential.oauth2.auth_response_uri = auth_response_uri
    auth_config.exchanged_auth_credential.oauth2.redirect_uri = redirect_uri

    auth_content = types.Content(
        role="user",
        parts=[
            types.Part(
                function_response=types.FunctionResponse(
                    id=auth_function_call_id,
                    name="adk_request_credential",
                    response=auth_config.model_dump(),
                )
            )
        ],
    )

    # Second run: ADK exchanges code for tokens, retries the tool
    async for event in runner.run_async(
        session_id=session.id, user_id="user", new_message=auth_content
    ):
        yield event
