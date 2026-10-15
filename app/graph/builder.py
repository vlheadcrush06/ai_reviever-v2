"""Построение графа импортов."""

import networkx as nx


def resolve_import(imp: str, modules: set) -> str | None:
    if imp in modules:
        return imp
    candidates = [m for m in modules if m.startswith(imp + ".")]
    if candidates:
        return min(candidates, key=len)
    return None


def build_graph(py_files) -> nx.DiGraph:
    modules = {f["module"] for f in py_files if f.get("module")}
    G = nx.DiGraph()

    for f in py_files:
        if not f.get("module"):
            continue
        G.add_node(f["module"])
        for imp in f.get("imports", []):
            target = resolve_import(imp, modules)
            if target and target != f["module"]:
                G.add_edge(f["module"], target)

    return G
