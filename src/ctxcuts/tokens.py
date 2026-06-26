"""Small token-ish estimators.

This intentionally avoids model-specific tokenizers in v0.1. The goal is a
useful directional estimate, not exact billing numbers.
"""

from __future__ import annotations

import math


def estimate_tokens(text: str) -> int:
    """Estimate tokens with a simple chars/4 heuristic."""
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


def estimate_savings(short_input: str, expanded: str, baseline: str | None = None) -> int:
    """Estimate percentage saved vs a manual baseline."""
    expanded_tokens = estimate_tokens(expanded)
    if baseline:
        baseline_tokens = estimate_tokens(baseline)
    else:
        baseline_tokens = max(expanded_tokens + estimate_tokens(short_input), expanded_tokens)

    if baseline_tokens <= 0:
        return 0
    saved = max(0, baseline_tokens - estimate_tokens(short_input))
    return round((saved / baseline_tokens) * 100)
