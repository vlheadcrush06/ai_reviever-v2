"""Вкладка 'AI-ревью'."""

from pathlib import Path

import streamlit as st

from app.llm.client import llm_call


def render(
    py_files, all_funcs, metrics, G, root_path, provider, model, api_key, ollama_url
):
    st.subheader("🤖 AI Code Review")

    if not py_files:
        st.info("Нет Python-файлов для ревью.")
        return

    col1, col2 = st.columns([3, 1])
    with col2:
        mode = st.radio("Режим", ["Один файл", "Проект целиком"])
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)

    with col1:
        if mode == "Один файл":
            _render_single_file(
                py_files, root_path, provider, model, api_key, ollama_url, temperature
            )
        else:
            _render_project(
                all_funcs,
                metrics,
                G,
                py_files,
                provider,
                model,
                api_key,
                ollama_url,
                temperature,
            )


def _render_single_file(
    py_files, root_path, provider, model, api_key, ollama_url, temperature
):
    file_options = [f["rel"] for f in py_files]
    selected = st.selectbox("Файл", file_options)
    task = st.selectbox(
        "Задача",
        [
            "Общий код-ревью: баги, стиль, читаемость",
            "Предложить рефакторинг",
            "Найти потенциальные баги и edge-cases",
            "Оценить архитектуру модуля",
        ],
    )

    if st.button("▶️ Запустить ревью", type="primary"):
        file_path = Path(root_path) / selected
        if not file_path.exists():
            st.error(
                "Файл недоступен — возможно, временная папка удалена. "
                "Перезапусти анализ."
            )
            return

        src = file_path.read_text(encoding="utf-8", errors="ignore")
        system = (
            "Ты — senior software engineer. Отвечай кратко, "
            "по делу, на русском. Используй markdown."
        )
        user = f"Задача: {task}\nФайл: {selected}\n\n```python\n{src[:12000]}\n```"

        with st.spinner("LLM думает..."):
            out = llm_call(
                provider, model, api_key, ollama_url, system, user, temperature
            )
        st.markdown(out)


def _render_project(
    all_funcs, metrics, G, py_files, provider, model, api_key, ollama_url, temperature
):
    task = st.selectbox(
        "Задача",
        [
            "Общий обзор архитектуры и качества кода",
            "Топ-5 проблем и как их решить",
            "Оценить поддерживаемость и предложить план рефакторинга",
        ],
    )

    if st.button("▶️ Запустить ревью проекта", type="primary"):
        summary = {
            "files": metrics["total_files"],
            "loc": metrics["total_loc"],
            "funcs": metrics["total_funcs"],
            "classes": metrics["total_classes"],
            "avg_complexity": round(metrics["avg_complexity"], 2),
            "docstring_coverage": round(metrics["docstring_coverage"], 2),
            "top_depended": (
                sorted(G.in_degree, key=lambda x: x[1], reverse=True)[:10]
                if G.number_of_nodes()
                else []
            ),
            "risky_functions": [
                {"file": fn["file"], "name": fn["name"], "complexity": fn["complexity"]}
                for fn in sorted(
                    all_funcs, key=lambda x: x["complexity"], reverse=True
                )[:15]
            ],
            "file_tree": [f["rel"] for f in py_files][:200],
        }
        system = (
            "Ты — senior software architect. Отвечай структурировано, "
            "на русском, с примерами."
        )
        user = f"Задача: {task}\n\nМетрики проекта:\n{summary}"

        with st.spinner("LLM анализирует проект..."):
            out = llm_call(
                provider, model, api_key, ollama_url, system, user, temperature
            )
        st.markdown(out)
