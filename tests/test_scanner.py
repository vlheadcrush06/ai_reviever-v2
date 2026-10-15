"""Тесты сканера файлов."""

from pathlib import Path

from app.repo.loader import iter_code_files


def test_finds_python_and_js(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1\n")
    (tmp_path / "b.js").write_text("let x = 1;\n")
    (tmp_path / "readme.md").write_text("# hi\n")

    found = sorted(p.name for p, _ in iter_code_files(tmp_path))
    assert found == ["a.py", "b.js"]


def test_skips_node_modules(tmp_path: Path):
    skip = tmp_path / "node_modules"
    skip.mkdir()
    (skip / "junk.py").write_text("nope\n")
    (tmp_path / "a.py").write_text("x = 1\n")

    found = list(iter_code_files(tmp_path))
    names = sorted(p.name for p, _ in found)

    # Должен найтись только a.py, junk.py из node_modules — пропущен
    assert names == ["a.py"]


def test_skips_hidden_files(tmp_path: Path):
    (tmp_path / ".hidden.py").write_text("secret\n")
    (tmp_path / "a.py").write_text("x = 1\n")

    found = list(iter_code_files(tmp_path))
    assert all(not p.name.startswith(".") for p, _ in found)
