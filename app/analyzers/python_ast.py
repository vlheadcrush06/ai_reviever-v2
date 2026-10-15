"""AST-анализ Python: функции, классы, импорты, сложность."""

import ast
import os
from pathlib import Path


def _cyclomatic(node) -> int:
    cc = 1
    for child in ast.walk(node):
        if isinstance(
            child,
            (
                ast.If,
                ast.For,
                ast.AsyncFor,
                ast.While,
                ast.ExceptHandler,
                ast.With,
                ast.AsyncWith,
            ),
        ):
            cc += 1
        elif isinstance(child, ast.BoolOp):
            cc += len(child.values) - 1
        elif isinstance(child, ast.comprehension):
            cc += 1 + len(child.ifs)
    return cc


def module_name_from_rel(rel: str) -> str:
    """
    mypackage/utils.py    -> mypackage.utils
    mypackage/__init__.py -> mypackage
    """
    mod = rel.replace(os.sep, ".").removesuffix(".py")
    if mod == "__init__":
        return "__init__"
    if mod.endswith(".__init__"):
        return mod[: -len(".__init__")]
    return mod


def analyze_python(path: Path, root: Path) -> dict:
    try:
        rel = str(path.relative_to(root))
    except Exception:
        rel = str(path)

    module_name = module_name_from_rel(rel)

    try:
        source = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {
            "rel": rel,
            "module": module_name,
            "error": str(e),
            "functions": [],
            "classes": [],
            "imports": [],
            "loc": 0,
            "syntax_error": None,
            "lang": "Python",
        }

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {
            "rel": rel,
            "module": module_name,
            "functions": [],
            "classes": [],
            "imports": [],
            "loc": len(source.splitlines()),
            "syntax_error": f"{e.msg} (line {e.lineno})",
            "lang": "Python",
        }

    functions, classes, imports = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = (node.end_lineno or node.lineno) - node.lineno + 1
            n_args = len(node.args.args) + len(node.args.kwonlyargs)
            functions.append(
                {
                    "name": node.name,
                    "module": module_name,
                    "file": rel,
                    "line": node.lineno,
                    "length": length,
                    "args": n_args,
                    "complexity": _cyclomatic(node),
                    "has_docstring": ast.get_docstring(node) is not None,
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                }
            )
        elif isinstance(node, ast.ClassDef):
            classes.append(
                {
                    "name": node.name,
                    "module": module_name,
                    "file": rel,
                    "line": node.lineno,
                    "methods": sum(
                        1
                        for b in node.body
                        if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef))
                    ),
                    "has_docstring": ast.get_docstring(node) is not None,
                }
            )
        elif isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                imports.append(node.module.split(".")[0])

    return {
        "rel": rel,
        "module": module_name,
        "loc": len(source.splitlines()),
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "has_module_doc": ast.get_docstring(tree) is not None,
        "syntax_error": None,
        "lang": "Python",
    }
