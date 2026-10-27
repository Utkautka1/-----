"""
Урок 01: Git Начало (Уровень 1: С нуля).

Задание для новичка:
  1. Укажи имя папки твоего репозитория в переменной REPO_DIR.
  2. Создай в ней git-репозиторий (команда `git init`).
  3. Создай файл README.md и сделай первый коммит.
"""

from pathlib import Path

# Директория твоего локального репозитория
# Можно создать прямо внутри папки урока: lessons/01_git_basics/my_first_repo
REPO_DIR = Path(__file__).resolve().parent / "my_first_repo"


def get_repo_path() -> Path:
    """Возвращает путь к проверяемому репозиторию."""
    return REPO_DIR
