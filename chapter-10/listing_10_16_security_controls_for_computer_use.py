#!/usr/bin/env python3
"""
Security Controls for Computer Use
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from playwright.async_api import async_playwright

class IsolatedPlaywrightComputer:
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--incognito",           # no saved state
                "--disable-extensions",  # no extension injection
            ]
        )
        # New context with no stored credentials or cookies
        self.context = await self.browser.new_context(
            ignore_https_errors=False,  # enforce TLS validation
        )
        return self
