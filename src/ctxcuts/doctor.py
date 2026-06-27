# Validation helpers for ctxcuts projects.

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from ctxcuts.config import CtxcutsConfig

Severity = Literal["error", "warning", "info"]

_PLACEHOLDER_BODY_PATTERN = re.compile(r"{{\s*(.*?)\s*}}")
_SIMPLE_PLACEHOLDER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_DEFAULT_PLACEHOLDER_PATTERN = re.compile(
    r"^(?P<key>[a-zA-Z_][a-zA-Z0-9_]*)"
    r"\s*\|\s*default:\s*"
    r"(?P<quote>['\"]).*?(?P=quote)$"
)

KNOWN_TEMPLATE_VARIABLES = {
    "target",
    "focus",
    "output",
    "mode",
    "shortcut",
}


@dataclass(frozen=True)
class DoctorIssue:
    severity: Severity
    subject: str
    message: str


@dataclass(frozen=True)
class DoctorReport:
    issues: list[DoctorIssue]

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "info")

    @property
    def ok(self) -> bool:
        return self.error_count == 0


def run_doctor(config: CtxcutsConfig) -> DoctorReport:
    issues: list[DoctorIssue] = []

    if not config.shortcuts:
        issues.append(
            DoctorIssue(
                severity="error",
                subject="shortcuts",
                message="No shortcuts configured.",
            )
        )
        return DoctorReport(issues=issues)

    for key in sorted(config.shortcuts):
        shortcut = config.shortcuts[key]
        subject = f"{config.defaults.prefix}{shortcut.key} ({shortcut.name})"

        if not shortcut.description:
            issues.append(
                DoctorIssue(
                    severity="warning",
                    subject=subject,
                    message="Shortcut has no description.",
                )
            )

        if not shortcut.mode:
            issues.append(
                DoctorIssue(
                    severity="warning",
                    subject=subject,
                    message="Shortcut has no mode.",
                )
            )

        if not shortcut.context.exists():
            issues.append(
                DoctorIssue(
                    severity="error",
                    subject=subject,
                    message=f"Context file does not exist: {shortcut.context}",
                )
            )
            continue

        try:
            context_text = shortcut.context.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(
                DoctorIssue(
                    severity="error",
                    subject=subject,
                    message=f"Could not read context file: {exc}",
                )
            )
            continue

        if not context_text.strip():
            issues.append(
                DoctorIssue(
                    severity="warning",
                    subject=subject,
                    message=f"Context file is empty: {shortcut.context}",
                )
            )
            continue

        issues.extend(_validate_placeholders(subject, context_text))

    if not issues:
        issues.append(
            DoctorIssue(
                severity="info",
                subject="project",
                message="No problems found.",
            )
        )

    return DoctorReport(issues=issues)


def _validate_placeholders(subject: str, context_text: str) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []

    for match in _PLACEHOLDER_BODY_PATTERN.finditer(context_text):
        body = match.group(1).strip()
        variable = _extract_variable(body)

        if variable is None:
            issues.append(
                DoctorIssue(
                    severity="warning",
                    subject=subject,
                    message=f"Unsupported template placeholder: {{{{ {body} }}}}",
                )
            )
            continue

        if variable not in KNOWN_TEMPLATE_VARIABLES and _has_no_default(body):
            issues.append(
                DoctorIssue(
                    severity="warning",
                    subject=subject,
                    message=(
                        f"Runtime template variable `{variable}` has no default. "
                        "Pass it with `--var` or add a default value."
                    ),
                )
            )

    return issues


def _extract_variable(body: str) -> str | None:
    if _SIMPLE_PLACEHOLDER_PATTERN.match(body):
        return body

    default_match = _DEFAULT_PLACEHOLDER_PATTERN.match(body)
    if default_match:
        return default_match.group("key")

    return None


def _has_no_default(body: str) -> bool:
    return _DEFAULT_PLACEHOLDER_PATTERN.match(body) is None
