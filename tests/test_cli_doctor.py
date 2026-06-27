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


def test_doctor_command_succeeds_for_default_config(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["doctor", "--root", str(tmp_path)])

    assert result.exit_code == 0
    assert "No problems found" in result.output


def test_doctor_command_fails_for_missing_context(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    (tmp_path / ".ctxcuts" / "contexts" / "review.md").unlink()
    runner = CliRunner()

    result = runner.invoke(app, ["doctor", "--root", str(tmp_path)])

    assert result.exit_code == 1
    assert "error" in result.output
    assert "does not exist" in result.output
