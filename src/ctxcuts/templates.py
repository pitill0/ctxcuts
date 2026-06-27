"""Tiny template helpers."""

from __future__ import annotations

import re

_SIMPLE_PATTERN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")
_DEFAULT_PATTERN = re.compile(
    r"{{\s*"
    r"(?P<key>[a-zA-Z_][a-zA-Z0-9_]*)"
    r"\s*\|\s*default:\s*"
    r"(?P<quote>['\"])(?P<default>.*?)(?P=quote)"
    r"\s*}}"
)


def render_template(text: str, values: dict[str, object]) -> str:
    """Render minimal {{ name }} placeholders.

    Supported syntax:

    - {{ target }}
    - {{ focus | default: "bugs and regressions" }}

    This intentionally stays tiny and dependency-free. It is not Jinja.
    """

    def replace_default(match: re.Match[str]) -> str:
        key = match.group("key")
        default = match.group("default")
        value = values.get(key, "")
        if value is None or value == "":
            return default
        return str(value)

    def replace_simple(match: re.Match[str]) -> str:
        key = match.group(1)
        value = values.get(key, "")
        if value is None:
            return ""
        return str(value)

    rendered = _DEFAULT_PATTERN.sub(replace_default, text)
    return _SIMPLE_PATTERN.sub(replace_simple, rendered)
