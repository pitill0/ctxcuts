"""Clipboard helpers."""

from __future__ import annotations


class ClipboardError(RuntimeError):
    """Raised when clipboard access fails."""


def copy_text(text: str) -> None:
    """Copy text to the system clipboard."""
    try:
        import pyperclip
    except ImportError as exc:
        raise ClipboardError(
            "Clipboard support requires `pyperclip`. Install ctxcuts with clipboard "
            "support or add pyperclip to your environment."
        ) from exc

    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as exc:
        raise ClipboardError(f"Could not copy to clipboard: {exc}") from exc
