"""
Урок 02: Git Ветвление (Уровень 3: Профи).

Бонусные требования:
  - Создание ветки new2 от new.
  - Применение git revert HEAD для отката коммита.
  - Слияние ветки через git rebase.
"""

from pathlib import Path

# Укажите путь к продвинутому репозиторию
REPO_DIR = Path(__file__).resolve().parent / "branch_advanced_repo"


def get_repo_path() -> Path:
    """Возвращает путь к проверяемому репозиторию."""
    return REPO_DIR
