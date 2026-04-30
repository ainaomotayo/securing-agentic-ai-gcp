#!/usr/bin/env python3
"""
12.8 Supply Chain Risk in Code Execution
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

import subprocess
subprocess.run(["pip", "install", "requests-exfil"], check=True)
import requests_exfil
