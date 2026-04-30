#!/usr/bin/env python3
"""
13.3 Cloud Trace: Distributed Tracing for Agent Invocations
Chapter 13 — Observability Events Audit

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import time
from typing import Optional, Any, Dict
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

# Configure OpenTelemetry with Cloud Trace exporter
provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(CloudTraceSpanExporter())
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("adk-agent")

# Track active spans per invocation
_active_spans: dict[str, Any] = {}


def trace_before_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    """Start a trace span before each tool call."""
    invocation_id = tool_context.invocation_id
    tool_name = tool.name if hasattr(tool, "name") else str(tool)

    span = tracer.start_span(
        f"tool:{tool_name}",
        attributes={
            "adk.invocation_id": invocation_id,
            "adk.agent_name": tool_context.agent_name,
            "adk.tool_name": tool_name,
            "adk.session_id": tool_context.invocation_context.session.id,
        }
    )
    _active_spans[f"{invocation_id}:{tool_name}"] = span
    return None


def trace_after_tool(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Any,
) -> Optional[Any]:
    """End the trace span after each tool call."""
    invocation_id = tool_context.invocation_id
    tool_name = tool.name if hasattr(tool, "name") else str(tool)
    span_key = f"{invocation_id}:{tool_name}"

    span = _active_spans.pop(span_key, None)
    if span:
        if isinstance(tool_response, dict) and "error" in tool_response:
            span.set_attribute("adk.outcome", "error")
            span.set_attribute("adk.error", str(tool_response.get("error", "")))
        else:
            span.set_attribute("adk.outcome", "success")
        span.end()

    return None
