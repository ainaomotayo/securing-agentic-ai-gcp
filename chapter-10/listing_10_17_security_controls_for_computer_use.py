#!/usr/bin/env python3
"""
Security Controls for Computer Use
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

def restrict_browser_navigation(tool_context, tool_name: str, tool_args: dict) -> dict | None:
    allowed_domains = tool_context.state.get("app:allowed_browser_domains", [])
    if tool_name in ("navigate", "click"):
        url = tool_args.get("url", "")
        if url and not any(url.startswith(f"https://{d}") for d in allowed_domains):
            return {"error": f"Navigation to {url} is outside the allowed domain list."}
    return None
