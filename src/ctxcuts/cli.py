"""ctxcuts command line interface."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ctxcuts.config import CONFIG_DIR, ConfigError, load_config
from ctxcuts.defaults import DEFAULT_CONTEXTS, DEFAULT_SHORTCUTS_YML
from ctxcuts.expand import expand_invocation
from ctxcuts.tokens import estimate_savings, estimate_tokens

app = typer.Typer(help="Portable context shortcuts for AI agent workflows.")
console = Console()
error_console = Console(stderr=True)


@app.command()
def init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing files."),
) -> None:
    """Create a default .ctxcuts directory."""
    root = Path.cwd()
    config_dir = root / CONFIG_DIR
    contexts_dir = config_dir / "contexts"
    shortcuts_path = config_dir / "shortcuts.yml"

    config_dir.mkdir(exist_ok=True)
    contexts_dir.mkdir(exist_ok=True)

    _write_file(shortcuts_path, DEFAULT_SHORTCUTS_YML, force=force)
    for filename, content in DEFAULT_CONTEXTS.items():
        _write_file(contexts_dir / filename, content, force=force)

    console.print(f"[green]Created[/green] {CONFIG_DIR}/ with default shortcuts.")


@app.command("list")
def list_shortcuts() -> None:
    """List configured shortcuts."""
    config = _load_or_exit()
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
def expand(invocation: str = typer.Argument(..., help="Shortcut invocation.")) -> None:
    """Expand a shortcut invocation into a prompt."""
    config = _load_or_exit()
    expanded = _expand_or_exit(invocation, config)
    console.print(expanded.content)


@app.command()
def stats(invocation: str = typer.Argument(..., help="Shortcut invocation.")) -> None:
    """Show a lightweight token estimate for an invocation."""
    config = _load_or_exit()
    expanded = _expand_or_exit(invocation, config)

    input_tokens = estimate_tokens(invocation)
    expanded_tokens = estimate_tokens(expanded.content)
    saving = estimate_savings(invocation, expanded.content)

    table = Table(title="ctxcuts stats")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Shortcut input tokens", str(input_tokens))
    table.add_row("Expanded prompt tokens", str(expanded_tokens))
    table.add_row("Context budget", str(config.defaults.token_budget))
    table.add_row("Budget used", f"{round((expanded_tokens / config.defaults.token_budget) * 100)}%")
    table.add_row("Estimated typing/context reuse saving", f"~{saving}%")
    console.print(table)


def _write_file(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        console.print(f"[yellow]Skipped existing[/yellow] {path}")
        return
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    console.print(f"[green]Wrote[/green] {path}")


def _load_or_exit():  # noqa: ANN202 - Typer command helper exits process.
    try:
        return load_config()
    except ConfigError as exc:
        error_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


def _expand_or_exit(invocation: str, config):  # noqa: ANN001, ANN202
    try:
        return expand_invocation(invocation, config)
    except (ConfigError, ValueError) as exc:
        error_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
