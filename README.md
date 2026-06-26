# ctxcuts

Portable context shortcuts for AI agent workflows.

`ctxcuts` is a tiny CLI that lets you define reusable context shortcuts like
`:r`, `:f`, `:s` or `:a` and expand them into focused prompts for coding agents,
chat assistants, CLIs and custom workflows.

The goal is simple: stop repeating long prompts and stop loading huge context
files for every task. Load only the context you need, when you need it.

```bash
ctxc expand ":r src/player.py"
ctxc expand ":s src/auth.py --focus input-validation"
ctxc expand ":i web player stops after switching stations"
```

## Why?

Before:

```text
Please investigate why the web player sometimes stops after switching stations.
Do not patch anything yet. Look for lifecycle problems, race conditions and
browser audio edge cases. Give me likely causes first.
```

After:

```text
:i web player stops after switching stations --focus lifecycle
```

`ctxcuts` expands that tiny instruction into a reusable context contract.

## Install for local development

This project is designed for `uv`, but it uses a standard `pyproject.toml`.

```bash
uv sync
uv run ctxc --help
```

Without `uv`, any modern Python workflow that understands `pyproject.toml` should
work.

## Quick start

Create default context shortcuts in your repo:

```bash
ctxc init
```

List available shortcuts:

```bash
ctxc list
```

Expand a shortcut:

```bash
ctxc expand ":r src/app.py"
```

Estimate token-ish savings:

```bash
ctxc stats ":r src/app.py"
```

Pipe into another tool:

```bash
ctxc expand ":r src/app.py" | codex
ctxc expand ":r src/app.py" | claude
ctxc expand ":r src/app.py" | aider
```

## Default shortcuts

| Shortcut | Name | Purpose |
| --- | --- | --- |
| `:r` | review | Review without editing |
| `:f` | fix | Fix a concrete issue with the smallest safe change |
| `:t` | tests | Work on tests, failures and regressions |
| `:d` | docs | Improve or generate documentation |
| `:s` | security | Look for security issues and unsafe assumptions |
| `:a` | audit | Perform a structured audit |
| `:q` | quality | Improve maintainability and long-term quality |
| `:p` | perf | Analyze performance, latency and bottlenecks |
| `:x` | explain | Explain before changing anything |
| `:m` | map | Build a compact map of a file, module or repo area |
| `:i` | investigate | Investigate an issue before proposing a fix |
| `:c` | commit | Prepare commit summary, diff review or changelog entry |

## Config layout

```text
.ctxcuts/
├── shortcuts.yml
└── contexts/
    ├── review.md
    ├── fix.md
    ├── tests.md
    ├── docs.md
    ├── security.md
    ├── audit.md
    ├── quality.md
    ├── perf.md
    ├── explain.md
    ├── map.md
    ├── investigate.md
    └── commit.md
```

## Example config

```yaml
version: 1

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
```

## Philosophy

`ctxcuts` is not an agent framework.

It is closer to an `.editorconfig` for agent context:

- small
- local-first
- portable
- versionable
- vendor-neutral
- easy to delete

Shortcuts are not magic commands. They are portable context contracts.
