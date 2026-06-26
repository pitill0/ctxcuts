"""Small token-ish estimators.

This intentionally avoids model-specific tokenizers in v0.1. The goal is a
useful directional estimate, not exact billing numbers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenStats:
    """Directional token statistics for a shortcut expansion."""

    shortcut_input_tokens: int
    expanded_prompt_tokens: int
    reusable_context_tokens: int
    typed_ratio_percent: int
    reusable_context_percent: int


def estimate_tokens(text: str) -> int:
    """Estimate tokens with a simple chars/4 heuristic."""
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


def estimate_token_stats(short_input: str, expanded: str) -> TokenStats:
    """Estimate token stats for a shortcut expansion.

    The main useful metric is not "API savings" by itself. The expanded prompt
    still has to be sent to the model unless another layer performs caching or
    context loading.

    What ctxcuts provides is reusable context: the user types a tiny invocation,
    while the project keeps the larger task contract versioned and reusable.
    """

    shortcut_input_tokens = estimate_tokens(short_input)
    expanded_prompt_tokens = estimate_tokens(expanded)
    reusable_context_tokens = max(0, expanded_prompt_tokens - shortcut_input_tokens)

    if expanded_prompt_tokens <= 0:
        typed_ratio_percent = 0
        reusable_context_percent = 0
    else:
        typed_ratio_percent = round(
            (shortcut_input_tokens / expanded_prompt_tokens) * 100
        )
        reusable_context_percent = round(
            (reusable_context_tokens / expanded_prompt_tokens) * 100
        )

    return TokenStats(
        shortcut_input_tokens=shortcut_input_tokens,
        expanded_prompt_tokens=expanded_prompt_tokens,
        reusable_context_tokens=reusable_context_tokens,
        typed_ratio_percent=typed_ratio_percent,
        reusable_context_percent=reusable_context_percent,
    )


def estimate_savings(
    short_input: str,
    expanded: str,
    baseline: str | None = None,
) -> int:
    """Estimate percentage saved vs a manual baseline.

    Kept for compatibility with the initial API. Prefer estimate_token_stats()
    for user-facing stats.
    """

    if baseline is None:
        stats = estimate_token_stats(short_input, expanded)
        return stats.reusable_context_percent

    baseline_tokens = estimate_tokens(baseline)
    if baseline_tokens <= 0:
        return 0

    shortcut_tokens = estimate_tokens(short_input)
    saved = max(0, baseline_tokens - shortcut_tokens)
    return round((saved / baseline_tokens) * 100)
