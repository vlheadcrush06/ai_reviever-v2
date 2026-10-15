"""Все константы проекта в одном месте."""

CODE_EXTS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".cpp": "C++",
    ".cc": "C++",
    ".hpp": "C++",
    ".h": "C++",
    ".c": "C",
    ".cs": "C#",
    ".php": "PHP",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".sh": "Shell",
}

SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    ".next",
    ".idea",
    ".vscode",
    "target",
    "vendor",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
}

BIG_GRAPH_THRESHOLD = 500
GIT_CLONE_TIMEOUT = 120
RISKY_COMPLEXITY = 10
