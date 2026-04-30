#!/usr/bin/env python3
"""
9.4 Inter-Agent State Sharing: What Leaks and What Does Not
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Application code: set authorization policy before the pipeline runs
def initialize_legal_pipeline_session(
    case_id: str,
    user_id: str,
    session_service
) -> Session:
    session = session_service.create_session(app_name="legal-pipeline")

    # Policy state: app: prefix; model cannot write these
    session.state["app:case_id"] = case_id
    session.state["app:permitted_agents"] = ["ResearchAgent", "DraftingAgent"]
    session.state["app:research_db_allowlist"] = [
        "westlaw.internal", "lexisnexis.internal", "approved-filings.internal"
    ]
    session.state["app:max_research_results"] = 10

    # User context: user: prefix, persistent across sessions
    session.state["user:user_id"] = user_id
    session.state["user:clearance_level"] = get_user_clearance(user_id)

    # No no-prefix state keys set by application code
    # Agents can write these, which is fine for ephemeral task data
    return session
