"""Тесты AST-анализа."""

import ast
import os
from pathlib import Path

from app.analyzers.python_ast import _cyclomatic, analyze_python, module_name_from_rel

SAMPLE = '''"""Module doc."""
import os
from pathlib import Path


def hello(name):
    """Say hi."""
    if name:
        print(name)
    return 0


class Greeter:
    """Class."""

    def greet(self):
        return "hi"
'''


def test_module_name_simple():
    assert module_name_from_rel("foo.py") == "foo"


def test_module_name_nested():
    assert module_name_from_rel(os.path.join("pkg", "bar.py")) == "pkg.bar"


def test_module_name_init():
    assert module_name_from_rel(os.path.join("pkg", "__init__.py")) == "pkg"


def test_module_name_deep_init():
    rel = os.path.join("a", "b", "__init__.py")
    assert module_name_from_rel(rel) == "a.b"


def test_cyclomatic_simple():
    tree = ast.parse("def f():\n    return 1\n")
    assert _cyclomatic(tree.body[0]) == 1


def test_cyclomatic_with_if():
    tree = ast.parse("def f(x):\n    if x:\n        return 1\n    return 0\n")
    assert _cyclomatic(tree.body[0]) == 2


def test_cyclomatic_full():
    src = """
def f(x, y):
    for i in range(x):
        if i and y:
            continue
    while x:
        x -= 1
    return x
"""
    tree = ast.parse(src)
    assert _cyclomatic(tree.body[0]) == 5


def test_analyze_python_basic(tmp_path: Path):
    f = tmp_path / "sample.py"
    f.write_text(SAMPLE)
    res = analyze_python(f, tmp_path)

    assert res["module"] == "sample"
    assert res["has_module_doc"] is True
    assert len(res["functions"]) == 2
    assert len(res["classes"]) == 1
    assert "os" in res["imports"]
    assert "pathlib" in res["imports"]
    assert res["syntax_error"] is None


def test_analyze_python_syntax_error(tmp_path: Path):
    f = tmp_path / "bad.py"
    f.write_text("def f(:\n    pass\n")
    res = analyze_python(f, tmp_path)
    assert res["syntax_error"] is not None
    assert not res["rel"].startswith("/")
