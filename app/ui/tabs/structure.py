"""Вкладка 'Структура'."""

import pandas as pd
import streamlit as st


def render(files, all_funcs):
    st.subheader("Дерево файлов")
    df_files = pd.DataFrame(
        [
            {
                "Файл": f["rel"],
                "LOC": f["loc"],
                "Функций": len(f.get("functions", [])),
                "Классов": len(f.get("classes", [])),
                "Синтаксис": "❌" if f.get("syntax_error") else "✅",
            }
            for f in files
        ]
    ).sort_values("LOC", ascending=False)
    st.dataframe(df_files, use_container_width=True, hide_index=True, height=400)

    st.subheader("Функции с наибольшей сложностью")
    if all_funcs:
        df_fn = (
            pd.DataFrame(all_funcs).sort_values("complexity", ascending=False).head(20)
        )
        st.dataframe(
            df_fn[
                [
                    "file",
                    "name",
                    "line",
                    "length",
                    "complexity",
                    "args",
                    "has_docstring",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Функции не найдены.")
