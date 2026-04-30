#!/usr/bin/env python3
"""
Application code: set authorization policy before the pipeline runs
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Research Agent tool: reads from app: state for policy, writes to temp: for results
def search_case_law(
    query: str,
    tool_context: ToolContext,
) -> dict:
    """Search approved legal databases for case law."""
    # Policy from app: prefix; model cannot override this
    allowed_dbs = tool_context.state.get("app:research_db_allowlist", [])
    max_results = tool_context.state.get("app:max_research_results", 5)

    # The tool enforces the policy; the model cannot override it
    results = search_legal_databases(
        query=query,
        databases=allowed_dbs,  # Restricted to approved databases
        limit=max_results,
    )

    # Store results in temp:, ephemeral and only for this invocation
    # Do NOT write to no-prefix keys shared with the Drafting Agent
    tool_context.state["temp:research_results"] = results

    return {"summary": summarize_results(results), "result_count": len(results)}
