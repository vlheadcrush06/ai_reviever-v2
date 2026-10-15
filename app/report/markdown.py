"""Сборка markdown-отчёта."""


def build_markdown_report(metrics, py_files, files, ext_counter, G) -> str:
    lines = ["# 🧠 AI Code Reviewer — Отчёт", ""]
    lines.append("## Метрики проекта")
    lines.append(f"- Файлов всего: **{len(files)}**")
    lines.append(f"- Python-файлов: **{metrics['total_files']}**")
    lines.append(f"- Строк кода (Python): **{metrics['total_loc']}**")
    lines.append(f"- Функций: **{metrics['total_funcs']}**")
    lines.append(f"- Классов: **{metrics['total_classes']}**")
    lines.append(f"- Средняя сложность: **{metrics['avg_complexity']:.2f}**")
    lines.append(f"- Средняя длина функции: **{metrics['avg_func_length']:.1f}** строк")
    lines.append(
        f"- Docstring coverage (функции): **{metrics['docstring_coverage']*100:.0f}%**"
    )
    lines.append(
        f"- Docstring coverage (модули): **{metrics['module_doc_ratio']*100:.0f}%**"
    )
    lines.append(f"- Syntax errors: **{metrics['syntax_errors']}**")
    lines.append(f"- Quality score: **{metrics['score']:.1f}/100**")
    if metrics.get("note"):
        lines.append(f"- ⓘ {metrics['note']}")
    lines.append("")

    lines.append("## Языки")
    for lang, count in sorted(ext_counter.items(), key=lambda x: -x[1]):
        lines.append(f"- {lang}: {count}")
    lines.append("")

    lines.append("## Топ-10 файлов по LOC")
    for f in sorted(files, key=lambda x: x["loc"], reverse=True)[:10]:
        lines.append(f"- `{f['rel']}` — {f['loc']} строк")
    lines.append("")

    all_funcs = [fn for f in py_files for fn in f.get("functions", [])]
    if all_funcs:
        lines.append("## Топ-10 самых сложных функций")
        for fn in sorted(all_funcs, key=lambda x: x["complexity"], reverse=True)[:10]:
            lines.append(
                f"- `{fn['file']}::{fn['name']}` — complexity {fn['complexity']}, "
                f"{fn['length']} строк (line {fn['line']})"
            )
        lines.append("")

    if G.number_of_nodes() > 0:
        lines.append("## Топ модулей по in-degree")
        for m, d in sorted(G.in_degree, key=lambda x: -x[1])[:10]:
            lines.append(f"- `{m}` — импортируется {d} раз(а)")
        lines.append("")
        lines.append("## Топ модулей по out-degree")
        for m, d in sorted(G.out_degree, key=lambda x: -x[1])[:10]:
            lines.append(f"- `{m}` — импортирует {d} модулей")

    return "\n".join(lines)
