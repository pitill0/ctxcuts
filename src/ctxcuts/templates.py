"""Tiny template helpers."""

from __future__ import annotations

import re

_PATTERN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")


def render_template(text: str, values: dict[str, object]) -> str:
    """Render {{ name }} placeholders using a minimal built-in renderer."""

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = values.get(key, "")
        return str(value)

    return _PATTERN.sub(replace, text)
