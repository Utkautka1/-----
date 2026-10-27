"""
Урок 01: Git Начало (Уровень 3: Профи).

Бонусные требования:
  - Наличие корректного .gitignore.
  - Наличие минимум 4 коммитов с осмысленными Conventional Commits префиксами.
"""

from pathlib import Path

# Укажите путь к репозиторию повышенной сложности
REPO_DIR = Path(__file__).resolve().parent / "project_advanced"


def get_repo_path() -> Path:
    """Возвращает путь к продвинутому репозиторию."""
    return REPO_DIR
