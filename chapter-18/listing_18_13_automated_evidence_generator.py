#!/usr/bin/env python3
"""
Automated Evidence Generator
Chapter 18 — Governance Compliance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import json
from datetime import datetime, timedelta
from google.cloud import logging_v2

def generate_compliance_evidence_package(
    project_id: str,
    agent_service_name: str,
    agent_id: str,
    days: int = 30,
) -> dict:
    """
    Queries Cloud Audit Logs and the Agent Registry to produce a structured
    evidence package for regulatory review.
    """
    client = logging_v2.Client(project=project_id)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    # Load agent registry entry
    agent_record = get_agent_from_registry(agent_id)

    evidence = {
        "generated_at": end_time.isoformat(),
        "agent_id": agent_id,
        "regulatory_classification": agent_record.get("regulatory_classification"),
        "review_period": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
        },
    }

    # Tool call metrics
    filter_str = (
        f'resource.type="cloud_run_revision" '
        f'AND resource.labels.service_name="{agent_service_name}" '
        f'AND jsonPayload.event_type="tool_call" '
        f'AND timestamp >= "{start_time.isoformat()}Z"'
    )
    tool_call_entries = list(client.list_entries(filter_=filter_str, max_results=10000))
    evidence["tool_call_count"] = len(tool_call_entries)

    # HITL confirmation metrics
    hitl_filter = filter_str.replace(
        '"tool_call"', '"hitl_confirmation"'
    )
    hitl_entries = list(client.list_entries(filter_=hitl_filter, max_results=1000))
    evidence["hitl_confirmations"] = len(hitl_entries)

    # Injection blocking metrics
    injection_filter = filter_str.replace(
        '"tool_call"', '"injection_blocked"'
    )
    injection_entries = list(client.list_entries(filter_=injection_filter, max_results=1000))
    evidence["injection_attempts_blocked"] = len(injection_entries)

    # GDPR erasure requests
    erasure_filter = filter_str.replace(
        '"tool_call"', '"right_of_erasure"'
    )
    erasure_entries = list(client.list_entries(filter_=erasure_filter, max_results=100))
    evidence["gdpr_erasure_requests"] = len(erasure_entries)
    evidence["gdpr_erasure_completed"] = sum(
        1 for e in erasure_entries
        if e.payload.get("status") == "completed"
    )

    return evidence
