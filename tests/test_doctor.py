from pathlib import Path

from ctxcuts.config import load_config
from ctxcuts.defaults import DEFAULT_CONTEXTS, DEFAULT_SHORTCUTS_YML
from ctxcuts.doctor import run_doctor


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


def test_doctor_reports_ok_for_default_config(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    config = load_config(tmp_path)

    report = run_doctor(config)

    assert report.ok
    assert report.error_count == 0


def test_doctor_reports_missing_context_as_error(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    (tmp_path / ".ctxcuts" / "contexts" / "review.md").unlink()
    config = load_config(tmp_path)

    report = run_doctor(config)

    assert not report.ok
    assert report.error_count == 1
    assert "does not exist" in report.issues[0].message


def test_doctor_reports_empty_context_as_warning(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    (tmp_path / ".ctxcuts" / "contexts" / "review.md").write_text(
        "",
        encoding="utf-8",
    )
    config = load_config(tmp_path)

    report = run_doctor(config)

    assert report.ok
    assert report.warning_count == 1
    assert "empty" in report.issues[0].message


def test_doctor_reports_unknown_template_variable_as_warning(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    (tmp_path / ".ctxcuts" / "contexts" / "review.md").write_text(
        "# Review\n\nProject: {{ project }}\n",
        encoding="utf-8",
    )
    config = load_config(tmp_path)

    report = run_doctor(config)

    assert report.ok
    assert report.warning_count == 1
    assert "Unknown template variable: project" in report.issues[0].message


def test_doctor_reports_unsupported_placeholder_as_warning(tmp_path: Path) -> None:
    write_ctxcuts_config(tmp_path)
    (tmp_path / ".ctxcuts" / "contexts" / "review.md").write_text(
        "# Review\n\nValue: {{ focus | upper }}\n",
        encoding="utf-8",
    )
    config = load_config(tmp_path)

    report = run_doctor(config)

    assert report.ok
    assert report.warning_count == 1
    assert "Unsupported template placeholder" in report.issues[0].message
