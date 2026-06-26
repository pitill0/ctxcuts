"""Shortcut expansion."""

from __future__ import annotations

from dataclasses import dataclass

from ctxcuts.config import ConfigError, CtxcutsConfig
from ctxcuts.parser import Invocation, parse_invocation
from ctxcuts.templates import render_template


@dataclass(frozen=True)
class ExpandedPrompt:
    invocation: Invocation
    title: str
    content: str


def expand_invocation(raw: str, config: CtxcutsConfig) -> ExpandedPrompt:
    """Expand a raw shortcut invocation into a prompt."""
    invocation = parse_invocation(raw, prefix=config.defaults.prefix)
    shortcut = config.shortcuts.get(invocation.shortcut)
    if shortcut is None:
        available = ", ".join(
            f"{config.defaults.prefix}{key}" for key in sorted(config.shortcuts)
        )
        raise ConfigError(
            f"Unknown shortcut `{config.defaults.prefix}{invocation.shortcut}`. "
            f"Available: {available}"
        )

    if not shortcut.context.exists():
        raise ConfigError(f"Missing context file: {shortcut.context}")

    context_text = shortcut.context.read_text(encoding="utf-8").strip()
    focus = invocation.options.get("focus", "")
    output = invocation.options.get("output", config.defaults.output)

    rendered_context = render_template(
        context_text,
        {
            "target": invocation.target,
            "focus": focus,
            "output": output,
            "mode": shortcut.mode,
            "shortcut": shortcut.name,
        },
    )

    option_lines = _format_options(invocation.options)
    target = invocation.target or "Not specified"

    content = f"""{rendered_context}

---

Shortcut: {config.defaults.prefix}{shortcut.key} ({shortcut.name})
Mode: {shortcut.mode}
Target: {target}
Output: {output}
{option_lines}

User request:
{invocation.raw}
""".strip()

    return ExpandedPrompt(
        invocation=invocation,
        title=f"{config.defaults.prefix}{shortcut.key} {shortcut.name}",
        content=content,
    )


def _format_options(options: dict[str, str | bool]) -> str:
    if not options:
        return "Options: none"
    lines = ["Options:"]
    for key, value in sorted(options.items()):
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)
