#!/usr/bin/env python3
"""
9.5 Schema Validation Between Pipeline Stages
Chapter 09 — Securing Multi Agent Systems

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from pydantic import BaseModel, ValidationError
from typing import List, Optional

class ResearchResult(BaseModel):
    """Expected schema for Research Agent output."""
    query: str
    case_count: int
    cases: List[dict]  # Each case: {"citation": str, "summary": str, "date": str}
    confidence: float  # 0.0 to 1.0

class ResearchOutputValidator:
    """Validates Research Agent output before passing to Drafting Agent."""

    @staticmethod
    def validate(raw_output: str) -> Optional[ResearchResult]:
        """Parse and validate research output. Returns None if invalid."""
        import json
        try:
            data = json.loads(raw_output)
            result = ResearchResult(**data)

            # Additional semantic checks
            if result.confidence < 0.7:
                return None  # Too uncertain to use

            if result.case_count != len(result.cases):
                return None  # Inconsistent count

            return result
        except (json.JSONDecodeError, ValidationError, KeyError):
            return None
