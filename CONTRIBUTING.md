# Contributing

`ctxcuts` is intentionally small. Contributions should preserve that spirit.

Good additions:

- clearer context templates
- safer parsing
- better token estimates
- simple adapters that keep stdout/stdin workflows portable
- documentation with real examples

Avoid in early versions:

- background daemons
- cloud services
- vector databases
- vendor lock-in
- heavy agent orchestration

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy src
```
