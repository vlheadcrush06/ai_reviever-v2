"""Тесты графа зависимостей."""

from app.graph.builder import build_graph, resolve_import


def test_resolve_exact():
    mods = {"pkg", "pkg.utils"}
    assert resolve_import("pkg", mods) == "pkg"


def test_resolve_nested():
    mods = {"pkg", "pkg.utils", "pkg.other"}
    assert resolve_import("pkg.utils", mods) == "pkg.utils"


def test_resolve_missing():
    assert resolve_import("numpy", {"pkg"}) is None


def test_build_graph():
    files = [
        {"module": "pkg", "imports": ["pkg.utils"]},
        {"module": "pkg.utils", "imports": []},
        {"module": "pkg.other", "imports": ["pkg"]},
    ]
    G = build_graph(files)
    assert G.number_of_nodes() == 3
    assert G.number_of_edges() == 2
    assert G.has_edge("pkg", "pkg.utils")
    assert G.has_edge("pkg.other", "pkg")
