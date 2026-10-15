[🇷🇺 Русский](README.md) | 🇬🇧 **English**

---

# 🧠 AI Code Reviewer & Repo Analytics Dashboard

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