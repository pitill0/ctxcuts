from ctxcuts.tokens import estimate_savings, estimate_token_stats, estimate_tokens


def test_estimate_tokens_empty_text() -> None:
    assert estimate_tokens("") == 0


def test_estimate_tokens_uses_chars_heuristic() -> None:
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2


def test_estimate_token_stats_tracks_reusable_context() -> None:
    stats = estimate_token_stats(":r app.py", "Review mode instructions for app.py")

    assert stats.shortcut_input_tokens > 0
    assert stats.expanded_prompt_tokens >= stats.shortcut_input_tokens
    assert (
        stats.reusable_context_tokens
        == stats.expanded_prompt_tokens - stats.shortcut_input_tokens
    )
    assert stats.typed_ratio_percent + stats.reusable_context_percent in {
        99,
        100,
        101,
    }


def test_estimate_savings_without_baseline_returns_reusable_context_percent() -> None:
    stats = estimate_token_stats(":r app.py", "Review mode instructions for app.py")

    assert estimate_savings(":r app.py", "Review mode instructions for app.py") == (
        stats.reusable_context_percent
    )


def test_estimate_savings_with_baseline_compares_against_manual_prompt() -> None:
    saving = estimate_savings(
        ":r app.py",
        "expanded content",
        baseline=(
            "Please review app.py carefully without editing it and focus on bugs, "
            "regressions and edge cases."
        ),
    )

    assert saving > 0
