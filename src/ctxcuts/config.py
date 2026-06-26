"""Configuration loading for ctxcuts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = ".ctxcuts"
CONFIG_FILE = "shortcuts.yml"


class ConfigError(RuntimeError):
    """Raised when ctxcuts configuration is missing or invalid."""


@dataclass(frozen=True)
class Defaults:
    prefix: str = ":"
    output: str = "markdown"
    token_budget: int = 800


@dataclass(frozen=True)
class Shortcut:
    key: str
    name: str
    context: Path
    description: str
    mode: str


@dataclass(frozen=True)
class CtxcutsConfig:
    root: Path
    defaults: Defaults
    shortcuts: dict[str, Shortcut]

    @property
    def config_dir(self) -> Path:
        return self.root / CONFIG_DIR


def find_project_root(start: Path | None = None) -> Path:
    """Find the nearest parent directory containing .ctxcuts/shortcuts.yml."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / CONFIG_DIR / CONFIG_FILE).exists():
            return candidate
    raise ConfigError(
        "Could not find .ctxcuts/shortcuts.yml. Run `ctxc init` first."
    )


def load_config(root: Path | None = None) -> CtxcutsConfig:
    """Load ctxcuts configuration from a project root."""
    project_root = root.resolve() if root else find_project_root()
    config_path = project_root / CONFIG_DIR / CONFIG_FILE

    if not config_path.exists():
        raise ConfigError(f"Missing config file: {config_path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ConfigError("Config file must contain a YAML mapping.")

    defaults = _parse_defaults(raw.get("defaults", {}))
    shortcuts = _parse_shortcuts(raw.get("shortcuts"), project_root)
    return CtxcutsConfig(root=project_root, defaults=defaults, shortcuts=shortcuts)


def _parse_defaults(raw_defaults: Any) -> Defaults:
    if raw_defaults is None:
        return Defaults()
    if not isinstance(raw_defaults, dict):
        raise ConfigError("`defaults` must be a mapping.")

    prefix = str(raw_defaults.get("prefix", ":"))
    output = str(raw_defaults.get("output", "markdown"))
    token_budget = int(raw_defaults.get("token_budget", 800))

    if not prefix:
        raise ConfigError("`defaults.prefix` cannot be empty.")
    if token_budget <= 0:
        raise ConfigError("`defaults.token_budget` must be positive.")

    return Defaults(prefix=prefix, output=output, token_budget=token_budget)


def _parse_shortcuts(raw_shortcuts: Any, root: Path) -> dict[str, Shortcut]:
    if not isinstance(raw_shortcuts, dict) or not raw_shortcuts:
        raise ConfigError("`shortcuts` must be a non-empty mapping.")

    parsed: dict[str, Shortcut] = {}
    for key, value in raw_shortcuts.items():
        shortcut_key = str(key)
        if not isinstance(value, dict):
            raise ConfigError(f"Shortcut `{shortcut_key}` must be a mapping.")

        try:
            name = str(value["name"])
            context = root / CONFIG_DIR / str(value["context"])
        except KeyError as exc:
            raise ConfigError(
                f"Shortcut `{shortcut_key}` is missing `{exc.args[0]}`."
            ) from exc

        description = str(value.get("description", ""))
        mode = str(value.get("mode", "default"))

        parsed[shortcut_key] = Shortcut(
            key=shortcut_key,
            name=name,
            context=context,
            description=description,
            mode=mode,
        )

    return parsed
