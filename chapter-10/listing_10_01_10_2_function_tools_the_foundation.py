#!/usr/bin/env python3
"""
10.2 Function Tools: The Foundation
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import FunctionTool, ToolContext
from typing import Optional
import re
import logging
import json
import hashlib

logger = logging.getLogger(__name__)

def search_product_catalog(
    query: str,
    category: Optional[str],
    max_results: int,
    tool_context: ToolContext,
) -> dict:
    """
    Search the product catalog.
    Production-hardened: validates inputs, sanitizes results, logs calls.
    """
    # Input validation: types, lengths, allowed values
    if not isinstance(query, str) or not query.strip():
        return {"error": "Query must be a non-empty string."}

    if len(query) > 200:
        return {"error": "Query too long. Maximum 200 characters."}

    ALLOWED_CATEGORIES = {"electronics", "clothing", "books", "home", "sports"}
    if category and category not in ALLOWED_CATEGORIES:
        return {"error": f"Invalid category. Allowed values: {', '.join(sorted(ALLOWED_CATEGORIES))}"}

    # Policy from app: state; enforces max results regardless of model request
    policy = tool_context.invocation_context.session.state.get("app:search_policy", {})
    effective_max = min(max_results, policy.get("max_results", 20))
    effective_max = max(1, effective_max)  # At least 1

    try:
        # Audit: log the call before executing (before external state change)
        logger.info(json.dumps({
            "event": "tool_call",
            "tool": "search_product_catalog",
            "args_hash": hashlib.sha256(f"{query}:{category}:{effective_max}".encode()).hexdigest()[:16],
            "session_id": tool_context.session.id,
        }))

        results = _catalog_search(query, category, effective_max)

        # Output sanitization: strip fields that should not reach the model
        sanitized = []
        for item in results:
            sanitized.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "category": item.get("category"),
                "price": item.get("price"),
                # Exclude: internal_id, cost_price, supplier_id, warehouse_location
            })

        return {"results": sanitized, "count": len(sanitized)}

    except Exception as exc:
        # Error handling: log the real error; return a safe message to the model
        logger.error(f"catalog search failed: {exc}", exc_info=True)
        return {
            "error": "Product search is temporarily unavailable. Please try again later."
            # Do NOT include: str(exc), traceback, database error details
        }


def _catalog_search(query: str, category: Optional[str], limit: int) -> list:
    """Internal: actual database call. Not exposed directly to ADK."""
    # Production implementation here
    return []
