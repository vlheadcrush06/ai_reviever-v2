"""
Точка входа для Streamlit.
Запуск из КОРНЯ проекта:
    streamlit run streamlit_app.py
"""

import sys
from pathlib import Path

# Добавляем корень проекта в sys.path, чтобы работали импорты "from app.*"
sys.path.insert(0, str(Path(__file__).parent))

from app.main import render  # noqa: E402

render()
