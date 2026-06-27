"""Shortcut input parsing."""

from __future__ import annotations

import shlex
from dataclasses import dataclass


class ParseError(ValueError):
    """Raised when a shortcut invocation cannot be parsed."""


@dataclass(frozen=True)
class Invocation:
    shortcut: str
    target: str
    options: dict[str, str | bool]
    raw: str


def parse_invocation(raw: str, prefix: str = ":") -> Invocation:
    """Parse an invocation like ':r src/app.py --focus security'."""
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
    index = 1
    while index < len(parts):
        item = parts[index]
        if item.startswith("--"):
            option_name = item[2:]
            if not option_name:
                raise ParseError("Empty option name.")
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
        raw=raw,
    )
