"""Точка входа приложения. Содержит функцию render()."""

import tempfile
from pathlib import Path

import streamlit as st

from app.analyzers.scanner import scan_repo
from app.core.state import cleanup_old_temp_dir, register_temp_dir
from app.core.utils import is_url
from app.graph.builder import build_graph
from app.metrics.quality import quality_metrics
from app.repo.loader import fetch_repo
from app.ui.sidebar import render_sidebar
from app.ui.tabs import ai_review, dependencies, overview, quality, structure


def render():
    """Главная функция — вызывается из streamlit_app.py."""
    st.set_page_config(page_title="AI Code Reviewer", page_icon="🧠", layout="wide")

    st.title("🧠 AI Code Reviewer & Repo Analytics")
    st.caption("Анализ структуры, зависимостей и качества кода с AI-ревью")

    source, analyze_btn, provider, api_key, model, ollama_url = render_sidebar()

    if analyze_btn and source:
        _run_analysis(source)

    if "files" not in st.session_state:
        st.info("👈 Укажи GitHub URL или локальный путь и нажми **Анализировать**.")
        return

    _render_dashboard(provider, api_key, model, ollama_url)


def _run_analysis(source: str) -> None:
    """Загрузка репозитория + сканирование."""
    with st.spinner("Загружаю репозиторий..."):
        try:
            cleanup_old_temp_dir()

            if is_url(source):
                tmp = Path(tempfile.mkdtemp(prefix="repo_"))
                register_temp_dir(tmp)
                root = fetch_repo(source, tmp)
            else:
                root = fetch_repo(source, Path("."))

            st.session_state["root"] = str(root)

            progress_bar = st.progress(0, text="Сканирую файлы...")

            def _cb(done, total, current):
                pct = int(done / total * 100) if total else 100
                progress_bar.progress(pct, text=f"[{done}/{total}] {current}")

            files, ext_counter = scan_repo(root, progress_cb=_cb)

            progress_bar.empty()
            st.session_state["files"] = files
            st.session_state["ext_counter"] = dict(ext_counter)
            st.success(f"✅ Проанализировано {len(files)} файлов")
        except Exception as e:
            st.error(f"Ошибка: {e}")


def _render_dashboard(provider, api_key, model, ollama_url) -> None:
    """Отрисовка вкладок."""
    files = st.session_state["files"]
    ext_counter = st.session_state["ext_counter"]
    py_files = [f for f in files if f.get("module")]
    metrics = quality_metrics(py_files)
    G = build_graph(py_files)
    all_funcs = [fn for f in py_files for fn in f.get("functions", [])]

    tabs = st.tabs(
        ["📊 Обзор", "📁 Структура", "🕸️ Зависимости", "🎯 Качество", "🤖 AI-ревью"]
    )

    with tabs[0]:
        overview.render(metrics, files, ext_counter, py_files, G)
    with tabs[1]:
        structure.render(files, all_funcs)
    with tabs[2]:
        dependencies.render(G)
    with tabs[3]:
        quality.render(metrics, all_funcs)
    with tabs[4]:
        ai_review.render(
            py_files,
            all_funcs,
            metrics,
            G,
            st.session_state["root"],
            provider,
            model,
            api_key,
            ollama_url,
        )
