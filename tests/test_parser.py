from ctxcuts.parser import parse_invocation


def test_parse_invocation_with_target() -> None:
    invocation = parse_invocation(":r src/app.py")

    assert invocation.shortcut == "r"
    assert invocation.target == "src/app.py"
    assert invocation.options == {}


def test_parse_invocation_with_options() -> None:
    invocation = parse_invocation(":s src/auth.py --focus input-validation --strict")

    assert invocation.shortcut == "s"
    assert invocation.target == "src/auth.py"
    assert invocation.options == {"focus": "input-validation", "strict": True}
