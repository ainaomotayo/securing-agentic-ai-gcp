#!/usr/bin/env python3
"""
verify_environment.py — Checks installed package versions against book requirements.
Run before executing any chapter examples:
    python scripts/verify_environment.py
"""
import sys
import importlib.metadata as meta

REQUIREMENTS = {
    "google-adk": "1.0.0",
    "google-cloud-secret-manager": "2.20.0",
    "google-cloud-logging": "3.10.0",
    "google-cloud-aiplatform": "1.60.0",
    "google-auth": "2.29.0",
    "pydantic": "2.7.0",
}

def check_version(package: str, minimum: str) -> bool:
    try:
        installed = meta.version(package)
        from packaging.version import Version
        return Version(installed) >= Version(minimum)
    except meta.PackageNotFoundError:
        return False

if __name__ == "__main__":
    errors = []
    for pkg, min_ver in REQUIREMENTS.items():
        ok = check_version(pkg, min_ver)
        status = "OK " if ok else "FAIL"
        print(f"  [{status}] {pkg} >= {min_ver}")
        if not ok:
            errors.append(pkg)

    if errors:
        print(f"\nMissing or outdated: {', '.join(errors)}")
        print("Run: pip install -r requirements/requirements.txt")
        sys.exit(1)
    else:
        print("\nAll requirements satisfied.")
        sys.exit(0)
