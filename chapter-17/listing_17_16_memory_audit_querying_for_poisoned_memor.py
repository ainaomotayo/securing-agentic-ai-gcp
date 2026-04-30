#!/usr/bin/env python3
"""
Memory Audit: Querying for Poisoned Memories
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from vertexai.preview import rag
import vertexai

async def audit_memory_writes(
    corpus_name: str,
    incident_start_iso: str,
    incident_end_iso: str,
) -> list[dict]:
    """Query the RAG corpus for files/chunks written during the incident window."""
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    corpus = rag.get_corpus(name=corpus_name)
    files = rag.list_rag_files(corpus_name=corpus_name)

    suspicious = []
    for rag_file in files:
        # Check if creation time falls in the incident window
        created = rag_file.create_time.isoformat()
        if incident_start_iso <= created <= incident_end_iso:
            suspicious.append({
                "rag_file_name": rag_file.name,
                "display_name": rag_file.display_name,
                "created": created,
                "file_status": str(rag_file.file_status),
            })

    return suspicious
