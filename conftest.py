"""Маркер корня проекта для pytest.

Этот файл говорит pytest: "корень проекта здесь, добавь его в sys.path".
Без него pytest не может найти пакет app.
"""

import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
sys.path.insert(0, str(Path(__file__).parent))
