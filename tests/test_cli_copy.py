from pathlib import Path
from typing import Any

from typer.testing import CliRunner

from ctxcuts.cli import app
from ctxcuts.defaults import DEFAULT_CONTEXTS, DEFAULT_SHORTCUTS_YML


def write_ctxcuts_config(root: Path) -> None:
    config_dir = root / ".ctxcuts"
    contexts_dir = config_dir / "contexts"
    contexts_dir.mkdir(parents=True)

    (config_dir / "shortcuts.yml").write_text(
        DEFAULT_SHORTCUTS_YML,
        encoding="utf-8",
    )

    for filename, content in DEFAULT_CONTEXTS.items():
        (contexts_dir / filename).write_text(content, encoding="utf-8")


def test_copy_command_copies_expanded_prompt(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    write_ctxcuts_config(tmp_path)
    copied: list[str] = []

    def fake_copy_text(text: str) -> None:
        copied.append(text)

    monkeypatch.setattr("ctxcuts.cli.copy_text", fake_copy_text)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["copy", "--root", str(tmp_path), ":r src/app.py --focus security"],
    )

    assert result.exit_code == 0
    assert "Copied expanded prompt to clipboard" in result.output
    assert len(copied) == 1
    assert "Review Mode" in copied[0]
    assert "Target: src/app.py" in copied[0]
    assert "Focus: security" in copied[0]


def test_copy_command_reports_clipboard_errors(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    write_ctxcuts_config(tmp_path)

    def fake_copy_text(_text: str) -> None:
        from ctxcuts.clipboard import ClipboardError

        raise ClipboardError("clipboard unavailable")

    monkeypatch.setattr("ctxcuts.cli.copy_text", fake_copy_text)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["copy", "--root", str(tmp_path), ":r src/app.py"],
    )

    assert result.exit_code == 1
    assert "clipboard unavailable" in result.output
