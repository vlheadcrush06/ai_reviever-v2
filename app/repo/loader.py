"""Клонирование GitHub-репозитория или чтение локальной папки."""

import os
import subprocess
from pathlib import Path
from typing import Iterator, Tuple

from app.core.config import CODE_EXTS, GIT_CLONE_TIMEOUT, SKIP_DIRS
from app.core.utils import is_url


def fetch_repo(source: str, workdir: Path) -> Path:
    source = source.strip()

    if is_url(source):
        target = workdir / "repo"
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", source, str(target)],
                check=True,
                capture_output=True,
                text=True,
                timeout=GIT_CLONE_TIMEOUT,
            )
        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or "").strip()
            raise RuntimeError(
                f"Не удалось склонировать репозиторий.\n\n```\n{stderr}\n```"
            ) from e
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Git clone завис дольше {GIT_CLONE_TIMEOUT} секунд.")
        return target

    p = Path(source).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Путь не найден: {p}")
    if not p.is_dir():
        raise NotADirectoryError(f"Это не папка: {p}")
    return p


def iter_code_files(root: Path) -> Iterator[Tuple[Path, str]]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
        ]
        for fn in filenames:
            if fn.startswith("."):
                continue
            ext = Path(fn).suffix.lower()
            if ext in CODE_EXTS:
                yield Path(dirpath) / fn, CODE_EXTS[ext]
