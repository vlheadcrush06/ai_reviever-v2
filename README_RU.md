🇷🇺 **Русский** | [🇬🇧 English](README.en.md)

---

# 🧠 AI Code Reviewer & Repo Analytics Dashboard

Интерактивный дашборд для анализа кода: строит граф зависимостей,
оценивает качество, находит проблемные места и делает AI-ревью
через OpenAI или локальный Ollama.

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