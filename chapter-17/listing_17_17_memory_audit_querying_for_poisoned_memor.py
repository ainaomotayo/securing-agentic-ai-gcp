#!/usr/bin/env python3
"""
Memory Audit: Querying for Poisoned Memories
Chapter 17 — Incident Response

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

async def delete_poisoned_memory(rag_file_name: str) -> None:
    """Delete a specific RAG file from the memory corpus."""
    rag.delete_rag_file(name=rag_file_name)
    logging.info("Deleted poisoned memory file: %s", rag_file_name)
