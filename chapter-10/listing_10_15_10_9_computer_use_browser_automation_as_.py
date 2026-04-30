#!/usr/bin/env python3
"""
10.9 Computer Use: Browser Automation as an Attack Surface
Chapter 10 — Tool Security

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk import Agent
from google.adk.tools.computer_use.computer_use_toolset import ComputerUseToolset
from .playwright import PlaywrightComputer

root_agent = Agent(
    model="gemini-2.5-computer-use-preview-10-2025",  # specific model required
    name="browser_agent",
    instruction="Complete web-based tasks using the browser.",
    tools=[
        ComputerUseToolset(computer=PlaywrightComputer(screen_size=(1280, 936)))
    ],
)
