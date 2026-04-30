#!/usr/bin/env python3
"""
LoopAgent with explicit termination conditions
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# In the Research Agent: explicit escalation for unsafe conditions
def research_legal_content(query: str, tool_context: ToolContext) -> dict:
    result = search_database(query)

    if result.contains_injection_patterns:
        # Return a structured escalation signal, not the compromised result
        return {
            "status": "escalation_required",
            "reason": "Retrieved content contains suspicious patterns",
            "safe_to_proceed": False,
        }

    return {"status": "success", "results": result.summaries}
