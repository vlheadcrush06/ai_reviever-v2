"""Левый сайдбар."""

import streamlit as st

from app.llm.client import HAS_OPENAI


def render_sidebar():
    """Возвращает настройки, введённые пользователем."""
    with st.sidebar:
        st.header("⚙️ Источник")
        source = st.text_input(
            "GitHub URL или локальный путь",
            placeholder="https://github.com/psf/requests или /home/user/project",
        )
        analyze_btn = st.button(
            "🚀 Анализировать", type="primary", use_container_width=True
        )

        st.divider()
        st.header("🤖 LLM")
        provider = st.radio("Провайдер", ["OpenAI", "Ollama"], horizontal=True)

        if provider == "OpenAI":
            if not HAS_OPENAI:
                st.warning("Пакет `openai` не установлен.\n\n`pip install openai`")
            api_key = st.text_input("API Key", type="password")
            model = st.text_input("Модель", value="gpt-4o-mini")
            ollama_url = ""
        else:
            api_key = ""
            model = st.text_input("Модель", value="llama3.1:8b")
            ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")

    return source, analyze_btn, provider, api_key, model, ollama_url
