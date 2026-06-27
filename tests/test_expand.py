from pathlib import Path

from ctxcuts.config import load_config
from ctxcuts.defaults import DEFAULT_CONTEXTS, DEFAULT_SHORTCUTS_YML
from ctxcuts.expand import expand_invocation


def test_expand_invocation(tmp_path: Path) -> None:
    config_dir = tmp_path / ".ctxcuts"
    contexts_dir = config_dir / "contexts"
    contexts_dir.mkdir(parents=True)
    (config_dir / "shortcuts.yml").write_text(DEFAULT_SHORTCUTS_YML, encoding="utf-8")
    for filename, content in DEFAULT_CONTEXTS.items():
        (contexts_dir / filename).write_text(content, encoding="utf-8")

    config = load_config(tmp_path)
    expanded = expand_invocation(":r src/app.py", config)

    assert "# Review Mode" in expanded.content
    assert "Target: src/app.py" in expanded.content
    assert "Shortcut: :r (review)" in expanded.content


def test_expand_invocation_renders_focus_and_output_options(tmp_path: Path) -> None:
    config_dir = tmp_path / ".ctxcuts"
    contexts_dir = config_dir / "contexts"
    contexts_dir.mkdir(parents=True)

    (config_dir / "shortcuts.yml").write_text(DEFAULT_SHORTCUTS_YML, encoding="utf-8")

    for filename, content in DEFAULT_CONTEXTS.items():
        (contexts_dir / filename).write_text(content, encoding="utf-8")

    config = load_config(tmp_path)
    expanded = expand_invocation(
        ":r src/app.py --focus security --output checklist",
        config,
    )

    assert "Target: src/app.py" in expanded.content
    assert "Focus: security" in expanded.content
    assert "Output: checklist" in expanded.content
    assert "- focus: security" in expanded.content
    assert "- output: checklist" in expanded.content


def test_expand_invocation_renders_template_defaults(tmp_path: Path) -> None:
    config_dir = tmp_path / ".ctxcuts"
    contexts_dir = config_dir / "contexts"
    contexts_dir.mkdir(parents=True)

    (config_dir / "shortcuts.yml").write_text(DEFAULT_SHORTCUTS_YML, encoding="utf-8")

    for filename, content in DEFAULT_CONTEXTS.items():
        (contexts_dir / filename).write_text(content, encoding="utf-8")

    config = load_config(tmp_path)
    expanded = expand_invocation(":r src/app.py", config)

    assert "Focus: bugs, regressions and edge cases" in expanded.content
    assert "Output: markdown" in expanded.content
