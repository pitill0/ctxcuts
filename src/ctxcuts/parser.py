"""Shortcut input parsing."""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass

_VARIABLE_NAME_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_RESERVED_VARIABLE_NAMES = {
    "target",
    "focus",
    "output",
    "mode",
    "shortcut",
}


class ParseError(ValueError):
    """Raised when a shortcut invocation cannot be parsed."""


@dataclass(frozen=True)
class Invocation:
    shortcut: str
    target: str
    options: dict[str, str | bool]
    variables: dict[str, str]
    raw: str


def parse_invocation(raw: str, prefix: str = ":") -> Invocation:
    """Parse an invocation like ':r src/app.py --focus security --var area=auth'."""
    parts = shlex.split(raw.strip())
    if not parts:
        raise ParseError("Invocation cannot be empty.")

    head = parts[0]
    if not head.startswith(prefix):
        raise ParseError(f"Invocation must start with `{prefix}`.")

    shortcut = head[len(prefix) :]
    if not shortcut:
        raise ParseError("Shortcut key cannot be empty.")

    target_parts: list[str] = []
    options: dict[str, str | bool] = {}
    variables: dict[str, str] = {}
    index = 1
    while index < len(parts):
        item = parts[index]
        if item.startswith("--"):
            option_name = item[2:]
            if not option_name:
                raise ParseError("Empty option name.")

            if option_name == "var":
                next_index = index + 1
                if next_index >= len(parts) or parts[next_index].startswith("--"):
                    raise ParseError("`--var` requires a value in `key=value` format.")

                key, value = _parse_variable(parts[next_index])
                variables[key] = value
                index += 2
                continue

            next_index = index + 1
            if next_index < len(parts) and not parts[next_index].startswith("--"):
                options[option_name] = parts[next_index]
                index += 2
            else:
                options[option_name] = True
                index += 1
        else:
            target_parts.append(item)
            index += 1

    return Invocation(
        shortcut=shortcut,
        target=" ".join(target_parts).strip(),
        options=options,
        variables=variables,
        raw=raw,
    )


def _parse_variable(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise ParseError("`--var` value must use `key=value` format.")

    key, value = raw.split("=", 1)
    if not key:
        raise ParseError("`--var` key cannot be empty.")

    if not _VARIABLE_NAME_PATTERN.match(key):
        raise ParseError(
            "`--var` key must start with a letter or underscore and contain only "
            "letters, numbers and underscores."
        )

    if key in _RESERVED_VARIABLE_NAMES:
        raise ParseError(f"`--var` cannot override reserved variable `{key}`.")

    return key, value
