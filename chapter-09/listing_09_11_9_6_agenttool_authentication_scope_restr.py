#!/usr/bin/env python3
"""
9.6 AgentTool: Authentication Scope Restriction
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import agent_tool

# Wrap the Research Agent as a tool with explicit interface
research_tool = agent_tool.AgentTool(agent=research_agent)
# The tool has a schema: research_tool(query: str) -> dict

# The Coordinator calls it like any other tool
coordinator = LlmAgent(
    name="LegalCoordinator",
    model="gemini-2.0-flash",
    instruction="""You coordinate legal work. Use the research_tool to search for 
    case law. Use the draft_tool to create documents from research summaries.
    Do not call these tools with unvalidated user input; extract the specific
    search query or document type from the user's request first.""",
    tools=[research_tool, draft_tool],
    # No sub_agents; delegation is via tools, not LLM transfer
)
