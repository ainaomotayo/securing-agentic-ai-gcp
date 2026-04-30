#!/usr/bin/env python3
"""
Memory Expiration
Chapter 11 — Session State Memory Data Governance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from datetime import datetime, timedelta

MEMORY_RETENTION_DAYS = 90

def should_include_memory(memory, current_time: datetime) -> bool:
    if not hasattr(memory, "created_at"):
        return True  # Older memories without timestamps: include by default
    age = current_time - memory.created_at
    return age.days <= MEMORY_RETENTION_DAYS
