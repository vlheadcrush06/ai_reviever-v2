"""Работа с session_state Streamlit."""

import shutil
from pathlib import Path

import streamlit as st


def register_temp_dir(p: Path) -> None:
    if "app_created_dirs" not in st.session_state:
        st.session_state["app_created_dirs"] = []
    st.session_state["app_created_dirs"].append(str(p))


def cleanup_old_temp_dir() -> None:
    """Удаляем только СВОИ временные папки."""
    created = st.session_state.get("app_created_dirs", [])
    for p in created:
        path = Path(p)
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
    st.session_state["app_created_dirs"] = []
