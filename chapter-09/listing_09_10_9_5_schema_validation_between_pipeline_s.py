#!/usr/bin/env python3
"""
9.5 Schema Validation Between Pipeline Stages
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

# Coordinator's tool that calls Research Agent, validates, then passes to Drafting Agent
def research_and_draft(
    research_query: str,
    document_type: str,
    tool_context: ToolContext,
) -> dict:
    """Orchestrate research then drafting with schema validation between stages."""

    # Step 1: Call Research Agent (could be via AgentTool)
    raw_research = call_research_agent(research_query)

    # Step 2: Validate the research output before trusting it
    validated = ResearchOutputValidator.validate(raw_research)
    if validated is None:
        return {
            "error": "Research output did not meet validation requirements. "
                     "The research has been discarded. Please retry."
        }

    # Step 3: Pass validated, structured data to Drafting Agent
    # The Drafting Agent receives structured data, not raw model text
    draft = call_drafting_agent(
        research_summary=validated.model_dump(),  # Structured, validated
        document_type=document_type,
    )

    return {"draft": draft, "research_citations": [c["citation"] for c in validated.cases]}
