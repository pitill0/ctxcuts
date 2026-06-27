from ctxcuts.templates import render_template


def test_render_simple_placeholder() -> None:
    rendered = render_template("Target: {{ target }}", {"target": "src/app.py"})

    assert rendered == "Target: src/app.py"


def test_render_missing_placeholder_as_empty_string() -> None:
    rendered = render_template("Focus: {{ focus }}", {})

    assert rendered == "Focus: "


def test_render_default_placeholder_when_missing() -> None:
    rendered = render_template(
        'Focus: {{ focus | default: "bugs and regressions" }}',
        {},
    )

    assert rendered == "Focus: bugs and regressions"


def test_render_default_placeholder_when_empty() -> None:
    rendered = render_template(
        'Focus: {{ focus | default: "bugs and regressions" }}',
        {"focus": ""},
    )

    assert rendered == "Focus: bugs and regressions"


def test_render_default_placeholder_when_present() -> None:
    rendered = render_template(
        'Focus: {{ focus | default: "security" }}',
        {"focus": "performance"},
    )

    assert rendered == "Focus: performance"


def test_render_default_placeholder_accepts_single_quotes() -> None:
    rendered = render_template(
        "Output: {{ output | default: 'checklist' }}",
        {},
    )

    assert rendered == "Output: checklist"
