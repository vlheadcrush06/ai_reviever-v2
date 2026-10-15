"""Тесты утилит."""

from pathlib import Path

from app.core.utils import count_lines, is_url


def test_url_detection():
    assert is_url("https://github.com/x/y") is True
    assert is_url("http://x.y") is True
    assert is_url("git@github.com:x/y.git") is True


def test_local_path_detection():
    assert is_url("/home/user/proj") is False
    assert is_url("C:\\Users\\me\\proj") is False


def test_count_lines(tmp_path: Path):
    f = tmp_path / "x.py"
    f.write_text("a\nb\nc\n")
    assert count_lines(f) == 3


def test_count_lines_missing_file(tmp_path: Path):
    assert count_lines(tmp_path / "nope.py") == 0
