"""
Урок 02: Git Ветвление (Уровень 1: С нуля).

Задание для новичка:
  1. Создай репозиторий в папке REPO_DIR (команда `git init`).
  2. Сделай первый коммит в main.
  3. Создай ветку `new` (`git switch -c new` или `git checkout -b new`).
  4. Сделай коммит в ветке `new`.
  5. Вернись в `main` и влей ветку: `git merge new`.
"""

from pathlib import Path

# Укажите путь к рабочей папке с репозиторием
REPO_DIR = Path(__file__).resolve().parent / "branch_repo"


def get_repo_path() -> Path:
    """Возвращает путь к проверяемому репозиторию."""
    return REPO_DIR
