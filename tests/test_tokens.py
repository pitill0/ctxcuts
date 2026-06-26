from ctxcuts.tokens import estimate_tokens


def test_estimate_tokens_empty_text() -> None:
    assert estimate_tokens("") == 0


def test_estimate_tokens_short_text() -> None:
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2
