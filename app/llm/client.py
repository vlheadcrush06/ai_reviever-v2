"""Универсальный клиент для LLM."""

import requests
import streamlit as st

try:
    from openai import OpenAI

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@st.cache_data(show_spinner=False, ttl=3600)
def _cached_llm_call(provider, model, api_key, ollama_url, system, user, temperature):
    if provider == "OpenAI":
        if not HAS_OPENAI:
            return "❌ Пакет `openai` не установлен. Выполните: `pip install openai`"
        if not api_key:
            return "❌ Укажите OpenAI API key."
        try:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"❌ OpenAI error: {e}"

    if provider == "Ollama":
        try:
            r = requests.post(
                f"{ollama_url.rstrip('/')}/api/chat",
                json={
                    "model": model,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "options": {"temperature": temperature},
                },
                timeout=600,
            )
            r.raise_for_status()
            return r.json()["message"]["content"]
        except Exception as e:
            return f"❌ Ollama error: {e}"

    return "❌ Неизвестный провайдер."


def llm_call(provider, model, api_key, ollama_url, system, user, temperature=0.2):
    return _cached_llm_call(
        provider, model, api_key, ollama_url, system, user, temperature
    )
