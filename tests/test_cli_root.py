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


def test_list_uses_root_option(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["list", "--root", str(tmp_path)])

    assert result.exit_code == 0
    assert ":r" in result.output
    assert "review" in result.output


def test_expand_uses_root_option(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["expand", "--root", str(tmp_path), ":r src/app.py"],
    )

    assert result.exit_code == 0
    assert "Review Mode" in result.output
    assert "src/app.py" in result.output


def test_stats_uses_root_option(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["stats", "--root", str(tmp_path), ":r src/app.py"],
    )

    assert result.exit_code == 0
    assert "Reusable context portion" in result.output
    assert "Budget used" in result.output


def test_init_can_target_root(tmp_path: Path) -> None:
    target = tmp_path / "project"
    runner = CliRunner()

    result = runner.invoke(app, ["init", "--root", str(target)])

    assert result.exit_code == 0
    assert (target / ".ctxcuts" / "shortcuts.yml").exists()
    assert (target / ".ctxcuts" / "contexts" / "review.md").exists()
