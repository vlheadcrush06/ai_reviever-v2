"""Чистые функции — без Streamlit, без сети."""

from pathlib import Path


def is_url(source: str) -> bool:
    """URL это или локальный путь?"""
    return source.startswith(("http://", "https://", "git@"))


def count_lines(path: Path) -> int:
    """Безопасный подсчёт строк."""
    try:
        with path.open(encoding="utf-8", errors="ignore") as fh:
            return sum(1 for _ in fh)
    except Exception:
        return 0
