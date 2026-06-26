"""Default ctxcuts project files."""

from __future__ import annotations

DEFAULT_SHORTCUTS_YML = """version: 1

defaults:
  prefix: ":"
  output: markdown
  token_budget: 800

shortcuts:
  r:
    name: review
    context: contexts/review.md
    description: Review code or text without modifying it.
    mode: read_only

  f:
    name: fix
    context: contexts/fix.md
    description: Fix a concrete issue with the smallest safe change.
    mode: patch

  t:
    name: tests
    context: contexts/tests.md
    description: Work on tests, failures, coverage and regressions.
    mode: test

  d:
    name: docs
    context: contexts/docs.md
    description: Improve or generate documentation.
    mode: docs

  s:
    name: security
    context: contexts/security.md
    description: Look for security issues and unsafe assumptions.
    mode: read_only

  a:
    name: audit
    context: contexts/audit.md
    description: Perform a structured audit and produce findings.
    mode: read_only

  q:
    name: quality
    context: contexts/quality.md
    description: Improve maintainability, readability and long-term quality.
    mode: advisory

  p:
    name: perf
    context: contexts/perf.md
    description: Analyze performance, latency, memory and bottlenecks.
    mode: advisory

  x:
    name: explain
    context: contexts/explain.md
    description: Explain how something works before changing anything.
    mode: read_only

  m:
    name: map
    context: contexts/map.md
    description: Build a compact map of a file, module or repo area.
    mode: read_only

  i:
    name: investigate
    context: contexts/investigate.md
    description: Investigate an issue before proposing a fix.
    mode: read_only

  c:
    name: commit
    context: contexts/commit.md
    description: Prepare a clean commit summary, diff review or changelog entry.
    mode: write_text
"""

DEFAULT_CONTEXTS: dict[str, str] = {
    "review.md": """# Review Mode

You are reviewing the target in read-only mode.

Rules:
- Do not modify files.
- Identify bugs, regressions, edge cases and unclear behavior.
- Prefer concrete findings over broad suggestions.
- Include file paths and line references when available.
- End with a short recommendation.
""",
    "fix.md": """# Fix Mode

You are fixing a specific issue.

Rules:
- Make the smallest safe change.
- Avoid unrelated refactors.
- Preserve existing behavior unless explicitly required.
- Explain the root cause.
- Include tests or verification steps.
""",
    "tests.md": """# Test Mode

You are working on tests.

Rules:
- Focus on failing or missing coverage.
- Prefer meaningful tests over brittle tests.
- Explain what behavior each test protects.
- Avoid testing implementation details unless necessary.
""",
    "docs.md": """# Documentation Mode

You are improving documentation.

Rules:
- Keep language clear and practical.
- Prefer examples.
- Do not overpromise features.
- Preserve the existing tone of the project.
""",
    "security.md": """# Security Mode

You are reviewing the target from a security perspective.

Rules:
- Do not modify files unless explicitly asked.
- Look for unsafe input handling, auth flaws, injection risks, insecure defaults, secret leakage and supply-chain risks.
- Separate confirmed issues from hypothetical risks.
- Prefer actionable findings.
- Include severity, affected area and recommended fix.
""",
    "audit.md": """# Audit Mode

You are performing a structured audit.

Rules:
- Work systematically.
- Group findings by severity.
- Distinguish blockers, risks, improvements and notes.
- Avoid rewriting the project.
- End with a prioritized action list.
""",
    "quality.md": """# Quality Mode

You are evaluating maintainability and long-term quality.

Rules:
- Look for unnecessary complexity, duplication, unclear naming, fragile abstractions and hard-to-test code.
- Prefer small improvements over broad rewrites.
- Respect the existing style.
- Explain trade-offs.
""",
    "perf.md": """# Performance Mode

You are analyzing performance.

Rules:
- Look for avoidable latency, unnecessary work, memory growth, blocking operations and inefficient loops.
- Do not guess benchmarks.
- Separate measured evidence from suspicion.
- Suggest simple profiling or verification steps.
""",
    "explain.md": """# Explain Mode

You are explaining how the target works before changing anything.

Rules:
- Do not modify files.
- Explain the current behavior first.
- Call out assumptions and unknowns.
- Use clear structure and practical examples.
- End with possible next steps only if useful.
""",
    "map.md": """# Map Mode

You are building a compact map of the target.

Rules:
- Do not modify files.
- Identify the main components, responsibilities and data flow.
- Keep the map compact.
- Mention important entry points and dependencies.
- Highlight areas that likely matter for future work.
""",
    "investigate.md": """# Investigate Mode

You are investigating an issue before proposing a fix.

Rules:
- Do not patch immediately.
- Form hypotheses and rank them by likelihood.
- Identify evidence that confirms or rejects each hypothesis.
- Suggest the smallest useful inspection or test.
- Only propose fixes after the likely root cause is clear.
""",
    "commit.md": """# Commit Mode

You are preparing commit-oriented text.

Rules:
- Summarize the change clearly.
- Separate what changed from why it changed.
- Keep commit messages concise and specific.
- Mention tests or verification when available.
- Avoid marketing language.
""",
}
