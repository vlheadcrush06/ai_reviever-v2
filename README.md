
---

# 🧠 AI Code Reviewer & Repo Analytics Dashboard

Интерактивный дашборд для анализа кода: строит граф зависимостей,
оценивает качество, находит проблемные места и делает AI-ревью
через OpenAI или локальный Ollama.

**(Проверить приложение можно по ссылке | You can check out the app via the link: https://f78ddrjwdtezbrwrvcgds3.streamlit.app)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-23%20passed-success)](#-тесты)

---

## 📖 Содержание

- [Что это](#-что-это)
- [Возможности](#-возможности)
- [Структура проекта](#-структура-проекта)
- [Установка](#-установка)
- [Запуск](#-запуск)
- [Использование](#-использование)
- [Настройка LLM](#-настройка-llm)
- [Метрики качества](#-метрики-качества)
- [Архитектура](#-архитектура)
- [Тесты](#-тесты)
- [Частые проблемы](#-частые-проблемы)
- [FAQ](#-faq)
- [Лицензия](#-лицензия)

---

## 🎯 Что это

Приложение на Python + Streamlit, которое:

1. **Клонирует** GitHub-репозиторий или читает **локальную папку** с кодом
2. **Парсит** структуру: файлы, функции, классы, импорты через AST
3. **Строит** интерактивный граф зависимостей между модулями
4. **Оценивает** качество кода (сложность, docstrings, длина функций)
5. **Показывает** дашборд с графиками и таблицами на Plotly
6. **Делает AI-ревью** через OpenAI или локальный Ollama

Подходит для:

- Быстрого «health-check» нового проекта
- Обзора чужого репозитория перед контрибьютингом
- Аудита собственного кода на техдолг
- Обучения: наглядный AST-анализ и метрики

---

## ✨ Возможности

### Анализ

- 🐍 **Глубокий AST-анализ Python**: функции, классы, импорты, docstrings, цикломатическая сложность
- 🌐 **Мультиязычность**: подсчёт LOC для JS, TS, Go, Rust, Java, C++, C#, PHP, Ruby, Kotlin, Swift, Shell
- 🕸️ **Граф зависимостей** между Python-модулями с поиском циклических зависимостей
- 🚩 **Автодетект проблем**: функции со сложностью ≥ 10, отсутствие docstring, syntax errors

### Интерфейс

- 📈 **Интерактивные графики Plotly**: круговая диаграмма языков, гистограмма сложности, сетевой граф
- 📋 **Таблицы**: все файлы, функции, зависимости
- 📥 **Экспорт отчёта** в Markdown одной кнопкой
- ⚡ **Прогресс-бар** при сканировании больших проектов
- 🎯 **5 вкладок**: Обзор, Структура, Зависимости, Качество, AI-ревью

### AI

- 🤖 **OpenAI** — gpt-4o-mini, gpt-4o и др.
- 🏠 **Ollama** — llama3.1, mistral, codellama, qwen и др. (бесплатно, локально)
- 💾 **Кэширование ответов** на 1 час — повторные запросы мгновенные
- 📝 **4 режима ревью**: общий обзор, рефакторинг, поиск багов, оценка архитектуры
- 🌍 **Ревью файла или всего проекта**

---

## 📁 Структура проекта

```
ai_reviever(v2)/
├── streamlit_app.py              # Точка входа для Streamlit
├── conftest.py                   # Маркер корня проекта для pytest
├── requirements.txt              # Зависимости проекта
├── requirements-dev.txt          # + инструменты разработки
├── .gitignore                    # Что не коммитить в git
├── README_RU.md                     # Этот файл (русский)
├── README_EN.md                  # Английская версия
│
├── app/                          # Основной код приложения
│   ├── __init__.py
│   ├── main.py                   # Функция render() — вся логика UI
│   │
│   ├── core/                     # Ядро: конфиг, утилиты, состояние
│   │   ├── __init__.py
│   │   ├── config.py             # Константы и настройки
│   │   ├── utils.py              # Чистые функции (is_url, count_lines)
│   │   └── state.py              # Работа с session_state Streamlit
│   │
│   ├── repo/                     # Загрузка репозитория
│   │   ├── __init__.py
│   │   └── loader.py             # git clone, обход файлов
│   │
│   ├── analyzers/                # Анализ исходного кода
│   │   ├── __init__.py
│   │   ├── python_ast.py         # AST-парсинг Python
│   │   └── scanner.py            # Скан всего проекта
│   │
│   ├── graph/                    # Граф зависимостей
│   │   ├── __init__.py
│   │   └── builder.py            # Построение графа импортов
│   │
│   ├── metrics/                  # Метрики качества
│   │   ├── __init__.py
│   │   └── quality.py            # Расчёт quality score
│   │
│   ├── report/                   # Генерация отчётов
│   │   ├── __init__.py
│   │   └── markdown.py           # Сборка markdown-отчёта
│   │
│   ├── llm/                      # Работа с LLM
│   │   ├── __init__.py
│   │   └── client.py             # OpenAI + Ollama
│   │
│   └── ui/                       # Streamlit-интерфейс
│       ├── __init__.py
│       ├── sidebar.py            # Левый сайдбар
│       └── tabs/                 # Вкладки дашборда
│           ├── __init__.py
│           ├── overview.py       # 📊 Обзор
│           ├── structure.py      # 📁 Структура
│           ├── dependencies.py   # 🕸️ Зависимости
│           ├── quality.py        # 🎯 Качество
│           └── ai_review.py      # 🤖 AI-ревью
│
├── tests/                        # Автотесты (23 шт.)
│   ├── __init__.py
│   ├── test_utils.py             # 4 теста: утилиты
│   ├── test_ast.py               # 9 тестов: AST-анализ
│   ├── test_scanner.py           # 3 теста: сканер файлов
│   ├── test_graph.py             # 4 теста: граф зависимостей
│   └── test_metrics.py           # 3 теста: метрики качества
│
└── venv/                         # Виртуальное окружение (не коммитится)
```

### Назначение модулей

| Папка | Что содержит | Аналог из классики |
|---|---|---|
| `app/core/` | Настройки, утилиты, состояние | `core/` (FastAPI) |
| `app/repo/` | Работа с git и файлами | `crud/` |
| `app/analyzers/` | Парсинг кода | `services/` |
| `app/graph/` | Построение структур данных | `models/` |
| `app/metrics/` | Агрегация и расчёты | `schemas/` |
| `app/report/` | Формирование вывода | `serializers/` |
| `app/llm/` | Внешние API | `clients/` |
| `app/ui/` | Интерфейс | `api/` + `templates/` |

---

## 💻 Установка

### Требования

- **Python 3.10+** — [скачать](https://www.python.org/downloads/)
  > ⚠️ Windows: при установке поставь галочку **«Add Python to PATH»**
- **Git** — [скачать](https://git-scm.com/downloads) — для клонирования репозиториев
- **8+ ГБ RAM** — если планируешь использовать Ollama

### Шаги

#### 1. Создай папку проекта

```bash
mkdir ai_reviever
cd ai_reviever
```

#### 2. Создай виртуальное окружение

```bash
python -m venv venv
```

Активируй:

```bash
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows cmd:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

> 💡 **Windows + PowerShell:** если ругается «running scripts is disabled»:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

#### 3. Установи зависимости

```bash
pip install -r requirements-dev.txt
```

#### 4. Проверь тестами

```bash
pytest tests/ -v
```

Ожидаемый результат: **23 passed**.

---

## 🚀 Запуск

### Обычный запуск

```bash
streamlit run streamlit_app.py
```

Что произойдёт:

1. В терминале появится:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```
2. Браузер откроется автоматически
3. Если не открылся — перейди вручную на [http://localhost:8501](http://localhost:8501)

### Остановка

Нажми **`Ctrl + C`** в терминале.

### Другой порт

Если 8501 занят:

```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 📖 Использование

### Анализ GitHub-репозитория

В сайдбаре введи URL:

```
https://github.com/psf/requests
```

Нажми **🚀 Анализировать**. Подожди 10–60 секунд.

### Анализ локальной папки

Введи абсолютный путь:

- **Windows:** `C:\Users\Владимир\Desktop\my-project`
- **macOS / Linux:** `/home/user/my-project`

> Приложение работает в режиме **read-only** — только читает файлы.

### Вкладки

| Вкладка | Что показывает |
|---|---|
| **📊 Обзор** | Метрики, языки, крупнейшие файлы, экспорт |
| **📁 Структура** | Таблица всех файлов и топ сложных функций |
| **🕸️ Зависимости** | Интерактивный граф, циклические зависимости |
| **🎯 Качество** | Проблемные функции, docstring coverage |
| **🤖 AI-ревью** | LLM-анализ файла или проекта |

### Экспорт отчёта

Вкладка **📊 Обзор** → кнопка **📥 Скачать отчёт (Markdown)**. Получишь `code_review_report.md`.

---

## 🤖 Настройка LLM

### Вариант A — OpenAI (платно, быстро)

1. Зайди на [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Создай ключ (начинается с `sk-...`) — показывается **один раз**
3. В сайдбаре:
   - Провайдер: **OpenAI**
   - API Key: `sk-...`
   - Модель: `gpt-4o-mini` (дёшево) / `gpt-4o` (умнее)

**Стоимость:** ~$0.002–0.01 за ревью одного файла с `gpt-4o-mini`.

### Вариант B — Ollama (бесплатно, локально)

1. Установи с [ollama.com/download](https://ollama.com/download)
2. В отдельном терминале:

   ```bash
   ollama pull llama3.1:8b
   ollama serve
   ```

3. В сайдбаре:
   - Провайдер: **Ollama**
   - Ollama URL: `http://localhost:11434`
   - Модель: `llama3.1:8b`

### Рекомендуемые модели

| Модель | Размер | Комментарий |
|---|---|---|
| `llama3.1:8b` | 4.7 ГБ | Хороший баланс |
| `qwen2.5-coder:7b` | 4.7 ГБ | Заточен под код |
| `deepseek-coder-v2:16b` | 8.9 ГБ | Лучшее качество |
| `codellama:13b` | 7.4 ГБ | Классика |

### Сравнение провайдеров

| Критерий | OpenAI | Ollama |
|---|---|---|
| Стоимость | ~$0.01/запрос | Бесплатно |
| Скорость | 5–20 сек | 20–90 сек |
| Качество | Высокое | Хорошее |
| Приватность | Код уходит на сервер | Всё локально |
| Нужен интернет | Да | Нет |

---

## 📊 Метрики качества

### Цикломатическая сложность (CC)

```
CC = 1 + if + for + while + except + with + (and/or - 1) + comprehensions
```

| CC | Оценка |
|---|---|
| 1–5 | ✅ Простая |
| 6–10 | 🟡 Умеренная |
| 11–20 | 🟠 Сложная |
| > 20 | 🔴 Требует рефакторинга |

### Quality Score (0–100)

```
score = 100
      − min(40, (avg_cc − 4) × 5)
      − (1 − docstring_coverage) × 20
      − min(20, (avg_func_length − 30) × 0.5)
      − (1 − module_doc_ratio) × 10
      − syntax_errors × 5
```

| Score | Оценка |
|---|---|
| 90–100 | 🟢 Отлично |
| 70–89 | 🟡 Хорошо |
| 50–69 | 🟠 Средне |
| 0–49 | 🔴 Плохо |

> ⚠️ Проект **без функций** (например, только конфиги) получает нейтральные **70/100**, а не 0.

---

## 🔬 Архитектура

```
┌────────────────┐    ┌──────────────┐    ┌─────────────┐
│ Источник       │───▶│ Сканирование │───▶│ AST-анализ  │
│ URL / папка    │    │ файлов       │    │ Python      │
└────────────────┘    └──────────────┘    └──────┬──────┘
                                                 │
                    ┌────────────────────────────┼──────────────────┐
                    ▼                            ▼                  ▼
            ┌──────────────┐           ┌─────────────────┐  ┌─────────────┐
            │ Граф         │           │ Метрики         │  │ Markdown-   │
            │ зависимостей │           │ качества        │  │ отчёт       │
            └──────┬───────┘           └────────┬────────┘  └─────────────┘
                   │                            │
                   └────────────┬───────────────┘
                                ▼
                        ┌──────────────┐
                        │ Streamlit UI │
                        │ + Plotly     │
                        └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ LLM-ревью    │
                        │ OpenAI/Ollama│
                        └──────────────┘
```

### Поток данных

1. **`streamlit_app.py`** — добавляет корень проекта в `sys.path`, вызывает `app.main.render()`
2. **`app.main.render()`** — настраивает UI, вызывает `sidebar.render_sidebar()`
3. **`app.repo.loader.fetch_repo()`** — клонирует или читает папку
4. **`app.analyzers.scanner.scan_repo()`** — обходит файлы, вызывает `analyze_python`
5. **`app.graph.builder.build_graph()`** — строит `networkx.DiGraph`
6. **`app.metrics.quality.quality_metrics()`** — считает метрики
7. **`app.ui.tabs.*`** — рисует 5 вкладок
8. **`app.llm.client.llm_call()`** — отправляет запрос в OpenAI / Ollama

---

## 🧪 Тесты

23 теста разбиты по модулям:

| Файл | Количество | Что проверяет |
|---|---|---|
| `test_utils.py` | 4 | `is_url`, `count_lines` |
| `test_ast.py` | 9 | `_cyclomatic`, `analyze_python`, `module_name_from_rel` |
| `test_scanner.py` | 3 | Обход файлов, фильтрация папок |
| `test_graph.py` | 4 | `resolve_import`, `build_graph` |
| `test_metrics.py` | 3 | `quality_metrics` для разных проектов |

### Запуск

```bash
pytest tests/ -v
```

Ожидаемый вывод:

```
tests/test_ast.py ............  9 passed
tests/test_graph.py ..........  4 passed
tests/test_metrics.py ........  3 passed
tests/test_scanner.py ........  3 passed
tests/test_utils.py ..........  4 passed

======================= 23 passed in 0.26s ======================
```

### Запуск одного теста

```bash
pytest tests/test_ast.py::test_cyclomatic_full -v -s
```

Флаг `-s` покажет `print` из тестов.

### Зачем `conftest.py` в корне

`conftest.py` сообщает pytest: «корень проекта здесь». Без него pytest не добавит корень в `sys.path`, и `from app.core...` будет падать с `ModuleNotFoundError`.

---

## 🚑 Частые проблемы

### `ModuleNotFoundError: No module named 'app'`

**При запуске pytest:** проверь, что `conftest.py` есть в корне проекта.

**При запуске Streamlit:** запускай через `streamlit run streamlit_app.py` (не `app/main.py`).

### `venv\Scripts\Activate.ps1 : Не удалось загрузить модуль "venv"`

Ты не в корне проекта. Проверь `pwd`, сделай `cd` в папку проекта.

В PowerShell нужна точка с `.\`:
```powershell
.\venv\Scripts\Activate.ps1
```

### `ModuleNotFoundError: No module named 'streamlit'`

venv не активирован. Проверь префикс `(venv)` в начале строки терминала.

### `Port 8501 is already in use`

```bash
streamlit run streamlit_app.py --server.port 8502
```

### `git: command not found`

Установи Git с [git-scm.com/downloads](https://git-scm.com/downloads).

### `Ollama error: connection refused`

Не запущен `ollama serve`. Запусти в отдельном терминале.

### Кракозябры в терминале Windows

```powershell
chcp 65001
```

Или: **Параметры → Время и язык → Административные языковые параметры → Изменить язык системы → Beta: Use Unicode UTF-8**.

---

## ❓ FAQ

**Безопасно ли указывать локальную папку?**
Да. Приложение работает в режиме read-only — только читает файлы.

**Отправляется ли мой код куда-то?**
OpenAI — да, при ревью. Ollama — нет, всё локально.

**Поддерживаются ли другие языки?**
Полный AST-анализ только для Python. Для остальных — LOC и участие в таблице.

**Почему граф пустой?**
Граф строится только для Python-модулей с импортами между собой. Сторонние библиотеки (numpy, requests) не создают рёбер.

**Можно ли ревьюить приватный репозиторий?**
Да, если настроен SSH-ключ: `git@github.com:user/repo.git`.

**Как очистить кэш LLM-ответов?**
Перезапусти приложение (Ctrl+C → снова `streamlit run`). Кэш живёт 1 час.

---

## 📄 Лицензия

MIT — используй свободно, в том числе в коммерческих проектах.

---

## 🙏 Благодарности

- [Streamlit](https://streamlit.io/) — UI
- [Plotly](https://plotly.com/python/) — графики
- [NetworkX](https://networkx.org/) — графы
- [OpenAI](https://openai.com/) и [Ollama](https://ollama.com/) — LLM

---

**Приятного ревью! 🚀**




An interactive dashboard for code analysis: builds a dependency graph,
evaluates code quality, detects problem areas, and performs AI-powered
reviews via OpenAI or local Ollama.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-23%20passed-success)](#-tests)

---

## 📖 Table of Contents

- [What is this](#-what-is-this)
- [Features](#-features)
- [Project structure](#-project-structure)
- [Installation](#-installation)
- [Running](#-running)
- [Usage](#-usage)
- [LLM setup](#-llm-setup)
- [Quality metrics](#-quality-metrics)
- [Architecture](#-architecture)
- [Tests](#-tests)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License](#-license)

---

## 🎯 What is this

A Python + Streamlit application that:

1. **Clones** a GitHub repository or reads a **local folder** with code
2. **Parses** the structure: files, functions, classes, imports via AST
3. **Builds** an interactive dependency graph between modules
4. **Evaluates** code quality (complexity, docstrings, function length)
5. **Displays** a dashboard with Plotly charts and tables
6. **Performs AI review** via OpenAI or local Ollama

Perfect for:

- Quick health-check of a new project
- Reviewing someone else's repo before contributing
- Auditing your own code for tech debt
- Learning: hands-on AST analysis and metrics

---

## ✨ Features

### Analysis

- 🐍 **Deep Python AST analysis**: functions, classes, imports, docstrings, cyclomatic complexity
- 🌐 **Multi-language**: LOC counting for JS, TS, Go, Rust, Java, C++, C#, PHP, Ruby, Kotlin, Swift, Shell
- 🕸️ **Dependency graph** between Python modules with cycle detection
- 🚩 **Auto-detection**: functions with complexity ≥ 10, missing docstrings, syntax errors

### UI

- 📈 **Interactive Plotly charts**: language pie chart, complexity histogram, network graph
- 📋 **Tables**: all files, functions, dependencies
- 📥 **One-click Markdown report export**
- ⚡ **Progress bar** during large-project scans
- 🎯 **5 tabs**: Overview, Structure, Dependencies, Quality, AI Review

### AI

- 🤖 **OpenAI** — gpt-4o-mini, gpt-4o, etc.
- 🏠 **Ollama** — llama3.1, mistral, codellama, qwen, etc. (free, local)
- 💾 **Response caching** for 1 hour — repeated requests are instant
- 📝 **4 review modes**: general overview, refactoring, bug hunting, architecture
- 🌍 **Review a single file or the whole project**

---

## 📁 Project structure

```
ai_reviever(v2)/
├── streamlit_app.py              # Streamlit entry point
├── conftest.py                   # pytest root marker
├── requirements.txt              # Project dependencies
├── requirements-dev.txt          # + dev tools
├── .gitignore                    # What not to commit
├── README_RU.md                     # Russian README
├── README_EN.md                  # This file (English)
│
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # render() — all UI logic
│   │
│   ├── core/                     # Core: config, utilities, state
│   │   ├── __init__.py
│   │   ├── config.py             # Constants and settings
│   │   ├── utils.py              # Pure functions (is_url, count_lines)
│   │   └── state.py              # Streamlit session_state handling
│   │
│   ├── repo/                     # Repository loading
│   │   ├── __init__.py
│   │   └── loader.py             # git clone, file iteration
│   │
│   ├── analyzers/                # Source code analysis
│   │   ├── __init__.py
│   │   ├── python_ast.py         # Python AST parsing
│   │   └── scanner.py            # Whole-project scan
│   │
│   ├── graph/                    # Dependency graph
│   │   ├── __init__.py
│   │   └── builder.py            # Import graph construction
│   │
│   ├── metrics/                  # Quality metrics
│   │   ├── __init__.py
│   │   └── quality.py            # Quality score calculation
│   │
│   ├── report/                   # Report generation
│   │   ├── __init__.py
│   │   └── markdown.py           # Markdown report builder
│   │
│   ├── llm/                      # LLM integration
│   │   ├── __init__.py
│   │   └── client.py             # OpenAI + Ollama
│   │
│   └── ui/                       # Streamlit interface
│       ├── __init__.py
│       ├── sidebar.py            # Left sidebar
│       └── tabs/                 # Dashboard tabs
│           ├── __init__.py
│           ├── overview.py       # 📊 Overview
│           ├── structure.py      # 📁 Structure
│           ├── dependencies.py   # 🕸️ Dependencies
│           ├── quality.py        # 🎯 Quality
│           └── ai_review.py      # 🤖 AI Review
│
├── tests/                        # Automated tests (23 items)
│   ├── __init__.py
│   ├── test_utils.py             # 4 tests: utilities
│   ├── test_ast.py               # 9 tests: AST analysis
│   ├── test_scanner.py           # 3 tests: file scanner
│   ├── test_graph.py             # 4 tests: dependency graph
│   └── test_metrics.py           # 3 tests: quality metrics
│
└── venv/                         # Virtual environment (not committed)
```

### Module overview

| Folder | Purpose | Classic equivalent |
|---|---|---|
| `app/core/` | Settings, utilities, state | `core/` (FastAPI) |
| `app/repo/` | Git and file handling | `crud/` |
| `app/analyzers/` | Code parsing logic | `services/` |
| `app/graph/` | Data structure building | `models/` |
| `app/metrics/` | Aggregation and computation | `schemas/` |
| `app/report/` | Output formatting | `serializers/` |
| `app/llm/` | External API integration | `clients/` |
| `app/ui/` | Interface layer | `api/` + `templates/` |

---

## 💻 Installation

### Requirements

- **Python 3.10+** — [download](https://www.python.org/downloads/)
  > ⚠️ Windows: enable **"Add Python to PATH"** during installation
- **Git** — [download](https://git-scm.com/downloads) — for cloning repositories
- **8+ GB RAM** — if you plan to use Ollama

### Steps

#### 1. Create the project folder

```bash
mkdir ai_reviever
cd ai_reviever
```

#### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows cmd:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

> 💡 **Windows + PowerShell:** if you see "running scripts is disabled":
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

#### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

#### 4. Run the tests

```bash
pytest tests/ -v
```

Expected: **23 passed**.

---

## 🚀 Running

### Standard run

```bash
streamlit run streamlit_app.py
```

What happens:

1. Terminal shows:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```
2. The browser opens automatically
3. If it doesn't — open [http://localhost:8501](http://localhost:8501)

### Stop

Press **`Ctrl + C`** in the terminal.

### Different port

```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 📖 Usage

### Analyze a GitHub repository

In the sidebar, enter a URL:

```
https://github.com/psf/requests
```

Click **🚀 Analyze**. Wait 10–60 seconds.

### Analyze a local folder

Enter the absolute path:

- **Windows:** `C:\Users\you\Desktop\my-project`
- **macOS / Linux:** `/home/user/my-project`

> The app runs in **read-only** mode — it only reads files.

### Tabs

| Tab | What it shows |
|---|---|
| **📊 Overview** | Metrics, languages, largest files, export |
| **📁 Structure** | Table of all files and top complex functions |
| **🕸️ Dependencies** | Interactive graph, cycles |
| **🎯 Quality** | Risky functions, docstring coverage |
| **🤖 AI Review** | LLM analysis of a file or the project |

### Export report

Tab **📊 Overview** → button **📥 Download report (Markdown)**. You get `code_review_report.md`.

---

## 🤖 LLM setup

### Option A — OpenAI (paid, fast)

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a key (starts with `sk-...`) — shown **only once**
3. In the sidebar:
   - Provider: **OpenAI**
   - API Key: `sk-...`
   - Model: `gpt-4o-mini` (cheap) / `gpt-4o` (smarter)

**Cost:** ~$0.002–0.01 per file review with `gpt-4o-mini`.

### Option B — Ollama (free, local)

1. Install from [ollama.com/download](https://ollama.com/download)
2. In a separate terminal:

   ```bash
   ollama pull llama3.1:8b
   ollama serve
   ```

3. In the sidebar:
   - Provider: **Ollama**
   - Ollama URL: `http://localhost:11434`
   - Model: `llama3.1:8b`

### Recommended models

| Model | Size | Note |
|---|---|---|
| `llama3.1:8b` | 4.7 GB | Good balance |
| `qwen2.5-coder:7b` | 4.7 GB | Tuned for code |
| `deepseek-coder-v2:16b` | 8.9 GB | Best quality |
| `codellama:13b` | 7.4 GB | Classic |

### Provider comparison

| Criterion | OpenAI | Ollama |
|---|---|---|
| Cost | ~$0.01/request | Free |
| Speed | 5–20 sec | 20–90 sec |
| Quality | High | Good |
| Privacy | Code leaves device | Fully local |
| Internet required | Yes | No |

---

## 📊 Quality metrics

### Cyclomatic complexity (CC)

```
CC = 1 + if + for + while + except + with + (and/or - 1) + comprehensions
```

| CC | Rating |
|---|---|
| 1–5 | ✅ Simple |
| 6–10 | 🟡 Moderate |
| 11–20 | 🟠 Complex |
| > 20 | 🔴 Needs refactoring |

### Quality Score (0–100)

```
score = 100
      − min(40, (avg_cc − 4) × 5)
      − (1 − docstring_coverage) × 20
      − min(20, (avg_func_length − 30) × 0.5)
      − (1 − module_doc_ratio) × 10
      − syntax_errors × 5
```

| Score | Rating |
|---|---|
| 90–100 | 🟢 Excellent |
| 70–89 | 🟡 Good |
| 50–69 | 🟠 Fair |
| 0–49 | 🔴 Poor |

> ⚠️ A project **without functions** (e.g. only configs) gets a neutral **70/100**, not 0.

---

## 🔬 Architecture

```
┌────────────────┐    ┌──────────────┐    ┌─────────────┐
│ Source         │───▶│ File         │───▶│ Python AST  │
│ URL / folder   │    │ scanning     │    │ analysis    │
└────────────────┘    └──────────────┘    └──────┬──────┘
                                                 │
                    ┌────────────────────────────┼──────────────────┐
                    ▼                            ▼                  ▼
            ┌──────────────┐           ┌─────────────────┐  ┌─────────────┐
            │ Dependency   │           │ Quality         │  │ Markdown    │
            │ graph        │           │ metrics         │  │ report      │
            └──────┬───────┘           └────────┬────────┘  └─────────────┘
                   │                            │
                   └────────────┬───────────────┘
                                ▼
                        ┌──────────────┐
                        │ Streamlit UI │
                        │ + Plotly     │
                        └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ LLM review   │
                        │ OpenAI/Ollama│
                        └──────────────┘
```

### Data flow

1. **`streamlit_app.py`** — adds the project root to `sys.path`, calls `app.main.render()`
2. **`app.main.render()`** — sets up UI, calls `sidebar.render_sidebar()`
3. **`app.repo.loader.fetch_repo()`** — clones or reads the folder
4. **`app.analyzers.scanner.scan_repo()`** — walks files, calls `analyze_python`
5. **`app.graph.builder.build_graph()`** — builds a `networkx.DiGraph`
6. **`app.metrics.quality.quality_metrics()`** — computes metrics
7. **`app.ui.tabs.*`** — renders 5 tabs
8. **`app.llm.client.llm_call()`** — sends request to OpenAI / Ollama

---

## 🧪 Tests

23 tests grouped by module:

| File | Count | What it checks |
|---|---|---|
| `test_utils.py` | 4 | `is_url`, `count_lines` |
| `test_ast.py` | 9 | `_cyclomatic`, `analyze_python`, `module_name_from_rel` |
| `test_scanner.py` | 3 | File iteration, folder filtering |
| `test_graph.py` | 4 | `resolve_import`, `build_graph` |
| `test_metrics.py` | 3 | `quality_metrics` for different projects |

### Run

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_ast.py ............  9 passed
tests/test_graph.py ..........  4 passed
tests/test_metrics.py ........  3 passed
tests/test_scanner.py ........  3 passed
tests/test_utils.py ..........  4 passed

======================= 23 passed in 0.26s ======================
```

### Run a single test

```bash
pytest tests/test_ast.py::test_cyclomatic_full -v -s
```

The `-s` flag shows `print` output from tests.

### Why `conftest.py` in the root

`conftest.py` tells pytest: "the project root is here". Without it, pytest won't add the root to `sys.path`, and `from app.core...` will fail with `ModuleNotFoundError`.

---

## 🚑 Troubleshooting

### `ModuleNotFoundError: No module named 'app'`

**When running pytest:** make sure `conftest.py` exists in the project root.

**When running Streamlit:** run via `streamlit run streamlit_app.py` (not `app/main.py`).

### `venv\Scripts\Activate.ps1 : Cannot load module "venv"`

You're not in the project root. Check `pwd`, run `cd` to the project folder.

In PowerShell, use `.\` prefix:
```powershell
.\venv\Scripts\Activate.ps1
```

### `ModuleNotFoundError: No module named 'streamlit'`

The venv is not activated. Check for the `(venv)` prefix in the terminal prompt.

### `Port 8501 is already in use`

```bash
streamlit run streamlit_app.py --server.port 8502
```

### `git: command not found`

Install Git from [git-scm.com/downloads](https://git-scm.com/downloads).

### `Ollama error: connection refused`

`ollama serve` isn't running. Start it in a separate terminal.

### Windows terminal encoding issues

```powershell
chcp 65001
```

Or: **Settings → Time & Language → Administrative language settings → Change system locale → Beta: Use Unicode UTF-8**.

---

## ❓ FAQ

**Is it safe to point to a local folder?**
Yes. The app is read-only — it only reads files.

**Is my code sent anywhere?**
OpenAI — yes, during review. Ollama — no, everything is local.

**Are other languages supported?**
Full AST analysis is Python-only. Other languages get LOC counts and appear in the table.

**Why is the graph empty?**
The graph only includes Python modules with imports between them. Third-party libraries (numpy, requests) don't create edges.

**Can I review a private repository?**
Yes, if an SSH key is configured: `git@github.com:user/repo.git`.

**How do I clear the LLM cache?**
Restart the app (Ctrl+C → `streamlit run` again). Cache lives for 1 hour.

---

## 📄 License

MIT — free to use, including commercial projects.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) — UI
- [Plotly](https://plotly.com/python/) — charts
- [NetworkX](https://networkx.org/) — graphs
- [OpenAI](https://openai.com/) and [Ollama](https://ollama.com/) — LLMs

---

**Happy reviewing! 🚀**
