"""Тесты метрик качества."""

from app.metrics.quality import quality_metrics


def test_empty_project():
    m = quality_metrics([])
    assert m["score"] == 100.0


def test_no_functions_project():
    files = [
        {
            "module": "a",
            "loc": 10,
            "functions": [],
            "classes": [],
            "syntax_error": None,
            "has_module_doc": True,
        }
    ]
    m = quality_metrics(files)
    assert m["score"] == 70.0
    assert m["note"] is not None


def test_good_project():
    files = [
        {
            "module": "a",
            "loc": 100,
            "functions": [
                {
                    "name": "f",
                    "file": "a.py",
                    "line": 1,
                    "length": 5,
                    "args": 0,
                    "complexity": 2,
                    "has_docstring": True,
                    "is_async": False,
                }
            ],
            "classes": [],
            "syntax_error": None,
            "has_module_doc": True,
        }
    ]
    m = quality_metrics(files)
    assert m["score"] >= 90
