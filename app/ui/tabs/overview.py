"""Вкладка 'Обзор'."""

import pandas as pd
import plotly.express as px
import streamlit as st

from app.report.markdown import build_markdown_report


def render(metrics, files, ext_counter, py_files, G):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Файлов", metrics["total_files"])
    c2.metric("Строк кода", f"{metrics['total_loc']:,}")
    c3.metric("Функций", metrics["total_funcs"])
    c4.metric("Классов", metrics["total_classes"])
    c5.metric("Quality score", f"{metrics['score']:.1f}/100")

    if metrics.get("note"):
        st.info(f"ⓘ {metrics['note']}")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Языки")
        df_lang = pd.DataFrame(
            {"Язык": list(ext_counter.keys()), "Файлов": list(ext_counter.values())}
        ).sort_values("Файлов", ascending=False)
        fig = px.pie(df_lang, names="Язык", values="Файлов", hole=0.5)
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Топ-10 самых больших файлов")
        df_big = (
            pd.DataFrame([{"Файл": f["rel"], "LOC": f["loc"]} for f in files])
            .sort_values("LOC", ascending=False)
            .head(10)
        )
        st.dataframe(df_big, use_container_width=True, hide_index=True)

    st.divider()
    report_md = build_markdown_report(metrics, py_files, files, ext_counter, G)
    st.download_button(
        "📥 Скачать отчёт (Markdown)",
        data=report_md,
        file_name="code_review_report.md",
        mime="text/markdown",
    )
