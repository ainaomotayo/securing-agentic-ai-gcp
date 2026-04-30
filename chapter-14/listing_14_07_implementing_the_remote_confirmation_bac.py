#!/usr/bin/env python3
"""
Implementing the Remote Confirmation Backend
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import asyncio
import json
from typing import AsyncGenerator
import httpx
from google.genai import types

async def run_with_remote_confirmation(
    runner,
    user_id: str,
    session_id: str,
    message: types.Content,
    approval_channel,  # Your approval notification system
) -> AsyncGenerator:
    """Run the agent, routing confirmation requests to remote approvers."""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        # Check if this is a confirmation request event
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (hasattr(part, "function_call")
                        and part.function_call
                        and part.function_call.name == "adk_request_confirmation"):

                    function_call_id = part.function_call.id
                    hint = part.function_call.args.get("hint", "")
                    payload_schema = part.function_call.args.get("payload", {})

                    # Route to the approver
                    approval_request = {
                        "function_call_id": function_call_id,
                        "session_id": session_id,
                        "user_id": user_id,
                        "hint": hint,
                        "payload_schema": payload_schema,
                    }

                    # Send to approval channel (Slack, email, dedicated UI)
                    await approval_channel.send_approval_request(approval_request)

                    # The agent is now paused; the approver will respond later
                    # Your application must store the session_id and function_call_id
                    # to route the response back when the approver decides
                    yield {"status": "pending_approval", "session_id": session_id}
                    return  # Wait for the remote response

        yield event


async def submit_approval_decision(
    adk_server_url: str,
    app_name: str,
    user_id: str,
    session_id: str,
    function_call_id: str,
    invocation_id: str,  # Required when using Resume feature
    approved: bool,
    reviewer_payload: dict,
    reviewer_notes: str,
) -> dict:
    """Submit an approver's decision to the ADK server."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{adk_server_url}/run_sse",
            json={
                "app_name": app_name,
                "user_id": user_id,
                "session_id": session_id,
                "invocation_id": invocation_id,
                "new_message": {
                    "role": "user",
                    "parts": [
                        {
                            "function_response": {
                                "id": function_call_id,
                                "name": "adk_request_confirmation",
                                "response": {
                                    "confirmed": approved,
                                    "payload": {
                                        **reviewer_payload,
                                        "reviewer_notes": reviewer_notes,
                                    },
                                },
                            }
                        }
                    ],
                },
            },
        )
        return response.json()
