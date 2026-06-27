import pytest

from ctxcuts.parser import ParseError, parse_invocation


def test_parse_invocation_with_target() -> None:
    invocation = parse_invocation(":r src/app.py")

    assert invocation.shortcut == "r"
    assert invocation.target == "src/app.py"
    assert invocation.options == {}
    assert invocation.variables == {}


def test_parse_invocation_with_options() -> None:
    invocation = parse_invocation(":s src/auth.py --focus input-validation --strict")

    assert invocation.shortcut == "s"
    assert invocation.target == "src/auth.py"
    assert invocation.options == {"focus": "input-validation", "strict": True}
    assert invocation.variables == {}


def test_parse_invocation_with_generic_variables() -> None:
    invocation = parse_invocation(
        ":r src/app.py --focus security --var area=auth --var risk=high"
    )

    assert invocation.shortcut == "r"
    assert invocation.target == "src/app.py"
    assert invocation.options == {"focus": "security"}
    assert invocation.variables == {"area": "auth", "risk": "high"}


def test_parse_invocation_allows_empty_variable_values() -> None:
    invocation = parse_invocation(":r src/app.py --var note=")

    assert invocation.variables == {"note": ""}


def test_parse_invocation_rejects_var_without_value() -> None:
    with pytest.raises(ParseError, match="requires a value"):
        parse_invocation(":r src/app.py --var")


def test_parse_invocation_rejects_var_without_equals() -> None:
    with pytest.raises(ParseError, match="key=value"):
        parse_invocation(":r src/app.py --var area")


def test_parse_invocation_rejects_invalid_var_key() -> None:
    with pytest.raises(ParseError, match="must start"):
        parse_invocation(":r src/app.py --var 1area=auth")


def test_parse_invocation_rejects_reserved_var_key() -> None:
    with pytest.raises(ParseError, match="reserved variable"):
        parse_invocation(":r src/app.py --var target=other")
