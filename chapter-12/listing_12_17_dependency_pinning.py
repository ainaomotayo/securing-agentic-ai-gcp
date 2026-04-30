#!/usr/bin/env python3
"""
Dependency Pinning
Chapter 12 — Secure Code Execution

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

APPROVED_PACKAGES = {
    "pandas": "2.2.2",
    "numpy": "1.26.4",
    "scipy": "1.13.0",
    "matplotlib": "3.8.4",
    "openpyxl": "3.1.2",
}

def install_approved_package(package_name: str) -> dict:
    if package_name not in APPROVED_PACKAGES:
        return {"error": f"Package '{package_name}' is not in the approved list."}
    version = APPROVED_PACKAGES[package_name]
    import subprocess
    result = subprocess.run(
        ["pip", "install", f"{package_name}=={version}", "--no-deps"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return {"error": f"Installation failed: {result.stderr}"}
    return {"status": "installed", "package": package_name, "version": version}
