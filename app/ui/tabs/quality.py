"""Вкладка 'Качество'."""

import pandas as pd
import plotly.express as px
import streamlit as st

from app.core.config import RISKY_COMPLEXITY


def render(metrics, all_funcs):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Средняя сложность", f"{metrics['avg_complexity']:.2f}")
    c2.metric("Средняя длина функции", f"{metrics['avg_func_length']:.1f} строк")
    c3.metric("Docstring coverage", f"{metrics['docstring_coverage']*100:.0f}%")
    c4.metric("Syntax errors", metrics["syntax_errors"])

    st.divider()
    st.subheader("Распределение сложности функций")

    if not all_funcs:
        st.info("Нет данных (в проекте нет Python-функций).")
        return

    df_fn = pd.DataFrame(all_funcs)
    fig = px.histogram(
        df_fn, x="complexity", nbins=30, color_discrete_sequence=["#4C78A8"]
    )
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"🚩 Проблемные функции (сложность ≥ {RISKY_COMPLEXITY})")
    risky = df_fn[df_fn["complexity"] >= RISKY_COMPLEXITY].sort_values(
        "complexity", ascending=False
    )
    if len(risky):
        st.dataframe(
            risky[["file", "name", "line", "complexity", "length"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("Функций с высокой сложностью не найдено 👍")

    st.subheader("📝 Функции без docstring")
    no_doc = df_fn[~df_fn["has_docstring"]]
    st.write(f"Всего: **{len(no_doc)}** из **{len(df_fn)}**")
    st.dataframe(
        no_doc[["file", "name", "line"]].head(50),
        use_container_width=True,
        hide_index=True,
    )
