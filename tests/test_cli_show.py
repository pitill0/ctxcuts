from pathlib import Path

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


def test_show_accepts_prefixed_shortcut(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["show", "--root", str(tmp_path), ":r"])

    assert result.exit_code == 0
    assert "review" in result.output
    assert "Review Mode" in result.output
    assert "read_only" in result.output


def test_show_accepts_plain_shortcut_key(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["show", "--root", str(tmp_path), "s"])

    assert result.exit_code == 0
    assert "security" in result.output
    assert "Security Mode" in result.output


def test_show_accepts_shortcut_name(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["show", "--root", str(tmp_path), "audit"])

    assert result.exit_code == 0
    assert "audit" in result.output
    assert "Audit Mode" in result.output


def test_show_fails_for_unknown_shortcut(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["show", "--root", str(tmp_path), ":missing"])

    assert result.exit_code == 1
    assert "Unknown shortcut" in result.output
    assert ":r" in result.output
