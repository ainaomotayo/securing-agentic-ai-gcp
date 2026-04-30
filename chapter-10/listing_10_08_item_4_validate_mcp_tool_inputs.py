#!/usr/bin/env python3
"""
Item 4: Validate MCP Tool Inputs
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

def validate_mcp_tool_args(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[Dict]:
    """Validate MCP tool arguments before execution."""
    if tool.name == "fetch_news":
        query = args.get("query", "")
        if not isinstance(query, str) or len(query) > 500:
            return {"error": "Invalid query argument for fetch_news."}
        # Block queries that look like injection attempts
        if re.search(r"(?:ignore|override|forget|disregard)\s+", query, re.IGNORECASE):
            return {"error": "Query contains disallowed terms."}

    if tool.name == "search_news":
        date_range = args.get("date_range", "")
        # Validate date format to prevent injection through date fields
        if date_range and not re.match(r"^\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}$", date_range):
            return {"error": "Invalid date_range format. Expected: YYYY-MM-DD/YYYY-MM-DD"}

    return None
