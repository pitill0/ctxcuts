# ctxcuts command line interface.

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ctxcuts.clipboard import ClipboardError, copy_text
from ctxcuts.config import CONFIG_DIR, ConfigError, CtxcutsConfig, Shortcut, load_config
from ctxcuts.defaults import DEFAULT_CONTEXTS, DEFAULT_SHORTCUTS_YML
from ctxcuts.doctor import run_doctor
from ctxcuts.expand import ExpandedPrompt, expand_invocation
from ctxcuts.tokens import estimate_token_stats

app = typer.Typer(help="Portable context shortcuts for AI agent workflows.")
console = Console()
error_console = Console(stderr=True)

RootOption = Annotated[
    Path | None,
    typer.Option(
        "--root",
        "-C",
        help="Project root containing .ctxcuts/. Defaults to the current directory.",
    ),
]


@app.command()
def init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing files."),
    root: RootOption = None,
) -> None:
    project_root = root or Path.cwd()
    project_root.mkdir(parents=True, exist_ok=True)

    config_dir = project_root / CONFIG_DIR
    contexts_dir = config_dir / "contexts"
    shortcuts_path = config_dir / "shortcuts.yml"

    config_dir.mkdir(exist_ok=True)
    contexts_dir.mkdir(exist_ok=True)

    _write_file(shortcuts_path, DEFAULT_SHORTCUTS_YML, force=force)
    for filename, content in DEFAULT_CONTEXTS.items():
        _write_file(contexts_dir / filename, content, force=force)

    console.print(f"[green]Created[/green] {config_dir} with default shortcuts.")


@app.command("list")
def list_shortcuts(root: RootOption = None) -> None:
    config = _load_or_exit(root)
    table = Table(title="ctxcuts shortcuts")
    table.add_column("Shortcut", style="bold")
    table.add_column("Name")
    table.add_column("Mode")
    table.add_column("Description")

    for key in sorted(config.shortcuts):
        shortcut = config.shortcuts[key]
        table.add_row(
            f"{config.defaults.prefix}{shortcut.key}",
            shortcut.name,
            shortcut.mode,
            shortcut.description,
        )

    console.print(table)


@app.command()
def expand(
    invocation: str = typer.Argument(..., help="Shortcut invocation."),
    root: RootOption = None,
) -> None:
    config = _load_or_exit(root)
    expanded = _expand_or_exit(invocation, config)
    console.print(expanded.content)


@app.command()
def copy(
    invocation: str = typer.Argument(..., help="Shortcut invocation."),
    root: RootOption = None,
) -> None:
    config = _load_or_exit(root)
    expanded = _expand_or_exit(invocation, config)

    try:
        copy_text(expanded.content)
    except ClipboardError as exc:
        error_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print("[green]Copied[/green] expanded prompt to clipboard.")


@app.command()
def doctor(root: RootOption = None) -> None:
    config = _load_or_exit(root)
    report = run_doctor(config)

    table = Table(title="ctxcuts doctor")
    table.add_column("Severity", style="bold")
    table.add_column("Subject")
    table.add_column("Message")

    for issue in report.issues:
        table.add_row(issue.severity, issue.subject, issue.message)

    console.print(table)

    if not report.ok:
        raise typer.Exit(code=1)


@app.command()
def show(
    shortcut_id: str = typer.Argument(
        ...,
        help="Shortcut key or name, for example ':r', 'r' or 'review'.",
    ),
    root: RootOption = None,
) -> None:
    config = _load_or_exit(root)
    shortcut = _resolve_shortcut_or_exit(shortcut_id, config)
    context_path = config.root / CONFIG_DIR / shortcut.context

    try:
        context = context_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        error_console.print(f"[red]Error:[/red] Context file not found: {context_path}")
        raise typer.Exit(code=1) from exc

    table = Table(title=f"ctxcuts shortcut {config.defaults.prefix}{shortcut.key}")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Name", shortcut.name)
    table.add_row("Mode", shortcut.mode)
    table.add_row("Context", str(context_path))
    table.add_row("Description", shortcut.description)
    console.print(table)
    console.print()
    console.print(context.rstrip())


def _resolve_shortcut_or_exit(
    shortcut_id: str,
    config: CtxcutsConfig,
) -> Shortcut:
    normalized = shortcut_id.strip()
    if normalized.startswith(config.defaults.prefix):
        normalized = normalized[len(config.defaults.prefix) :]

    if normalized in config.shortcuts:
        return config.shortcuts[normalized]

    for shortcut in config.shortcuts.values():
        if shortcut.name == normalized:
            return shortcut

    available = ", ".join(
        f"{config.defaults.prefix}{key}" for key in sorted(config.shortcuts)
    )
    error_console.print(
        f"[red]Error:[/red] Unknown shortcut '{shortcut_id}'. Available: {available}"
    )
    raise typer.Exit(code=1)


@app.command()
def stats(
    invocation: str = typer.Argument(..., help="Shortcut invocation."),
    root: RootOption = None,
) -> None:
    config = _load_or_exit(root)
    expanded = _expand_or_exit(invocation, config)
    token_stats = estimate_token_stats(invocation, expanded.content)

    budget_used = 0
    if config.defaults.token_budget > 0:
        budget_used = round(
            (token_stats.expanded_prompt_tokens / config.defaults.token_budget) * 100
        )

    table = Table(title="ctxcuts stats")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Shortcut input tokens", str(token_stats.shortcut_input_tokens))
    table.add_row("Expanded prompt tokens", str(token_stats.expanded_prompt_tokens))
    table.add_row("Reusable context tokens", str(token_stats.reusable_context_tokens))
    table.add_row("Typed portion", f"{token_stats.typed_ratio_percent}%")
    table.add_row(
        "Reusable context portion",
        f"{token_stats.reusable_context_percent}%",
    )
    table.add_row("Context budget", str(config.defaults.token_budget))
    table.add_row("Budget used", f"{budget_used}%")
    console.print(table)

    console.print(
        "\n[dim]Note: estimates use a simple chars/4 heuristic. "
        "ctxcuts reduces repeated typing and keeps reusable context versioned; "
        "actual model billing depends on the tool/provider and caching behavior.[/dim]"
    )


def _write_file(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        console.print(f"[yellow]Skipped existing[/yellow] {path}")
        return
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    console.print(f"[green]Wrote[/green] {path}")


def _load_or_exit(root: Path | None = None) -> CtxcutsConfig:
    try:
        return load_config(root=root)
    except ConfigError as exc:
        error_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


def _expand_or_exit(
    invocation: str,
    config: CtxcutsConfig,
) -> ExpandedPrompt:
    try:
        return expand_invocation(invocation, config)
    except (ConfigError, ValueError) as exc:
        error_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
