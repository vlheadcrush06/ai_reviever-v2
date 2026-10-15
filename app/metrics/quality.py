"""Расчёт quality score."""


def quality_metrics(py_files) -> dict:
    all_funcs = [fn for f in py_files for fn in f.get("functions", [])]
    all_classes = [c for f in py_files for c in f.get("classes", [])]
    total_loc = sum(f["loc"] for f in py_files)
    syntax_errors = sum(1 for f in py_files if f.get("syntax_error"))

    module_doc_ratio = (
        sum(1 for f in py_files if f.get("has_module_doc")) / len(py_files)
        if py_files
        else 0.0
    )

    if not all_funcs:
        return {
            "total_files": len(py_files),
            "total_loc": total_loc,
            "total_funcs": 0,
            "total_classes": len(all_classes),
            "avg_complexity": 0.0,
            "avg_func_length": 0.0,
            "docstring_coverage": 0.0,
            "module_doc_ratio": module_doc_ratio,
            "syntax_errors": syntax_errors,
            "score": 100.0 if not py_files else 70.0,
            "note": (
                "В проекте нет Python-функций — метрики сложности и "
                "docstring неприменимы, оценка нейтральная (70)."
                if py_files
                else "Python-файлы не найдены."
            ),
        }

    avg_cc = sum(fn["complexity"] for fn in all_funcs) / len(all_funcs)
    doc_cov = sum(fn["has_docstring"] for fn in all_funcs) / len(all_funcs)
    avg_len = sum(fn["length"] for fn in all_funcs) / len(all_funcs)

    score = 100.0
    score -= min(40, max(0, (avg_cc - 4) * 5))
    score -= (1 - doc_cov) * 20
    score -= min(20, max(0, (avg_len - 30) * 0.5))
    score -= (1 - module_doc_ratio) * 10
    score -= syntax_errors * 5
    score = max(0.0, min(100.0, score))

    return {
        "total_files": len(py_files),
        "total_loc": total_loc,
        "total_funcs": len(all_funcs),
        "total_classes": len(all_classes),
        "avg_complexity": avg_cc,
        "avg_func_length": avg_len,
        "docstring_coverage": doc_cov,
        "module_doc_ratio": module_doc_ratio,
        "syntax_errors": syntax_errors,
        "score": score,
        "note": None,
    }
