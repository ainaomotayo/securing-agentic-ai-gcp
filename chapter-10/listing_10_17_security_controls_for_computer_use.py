#!/usr/bin/env python3
"""
Security Controls for Computer Use
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext
from typing import Dict, Any, Optional

def restrict_browser_navigation(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[Dict]:
    allowed_domains = tool_context.state.get("app:allowed_browser_domains", [])
    if tool.name in ("navigate", "click"):
        url = args.get("url", "")
        if url and not any(url.startswith(f"https://{d}") for d in allowed_domains):
            return {"error": f"Navigation to {url} is outside the allowed domain list."}
    return None
