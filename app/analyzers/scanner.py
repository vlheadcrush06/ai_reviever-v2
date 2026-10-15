"""Скан всего проекта."""

from collections import Counter
from pathlib import Path
from typing import Callable, Optional

from app.analyzers.python_ast import analyze_python
from app.core.utils import count_lines
from app.repo.loader import iter_code_files


def scan_repo(
    root: Path, progress_cb: Optional[Callable[[int, int, str], None]] = None
):
    files, ext_counter = [], Counter()
    all_paths = list(iter_code_files(root))
    total = len(all_paths)

    for i, (path, lang) in enumerate(all_paths):
        if progress_cb:
            try:
                rel_display = str(path.relative_to(root))
            except Exception:
                rel_display = str(path)
            progress_cb(i + 1, total, rel_display)

        ext_counter[lang] += 1

        if lang == "Python":
            files.append(analyze_python(path, root))
        else:
            try:
                rel_display = str(path.relative_to(root))
            except Exception:
                rel_display = str(path)
            files.append(
                {
                    "rel": rel_display,
                    "module": None,
                    "loc": count_lines(path),
                    "functions": [],
                    "classes": [],
                    "imports": [],
                    "syntax_error": None,
                    "lang": lang,
                }
            )

    return files, ext_counter
