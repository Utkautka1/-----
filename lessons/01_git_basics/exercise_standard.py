"""
Урок 01: Git Начало (Уровень 2: Стандарт).

Требования университетской работы кафедры ЦАТ:
  - Репозиторий должен содержать минимум 3 коммита.
  - Наличие файлов: README.md, diff.txt, log.txt.
"""

from pathlib import Path

# Укажите путь к папке с вашим репозиторием
REPO_DIR = Path(__file__).resolve().parent / "project"


def get_repo_path() -> Path:
    """Возвращает путь к проверяемому репозиторию студента."""
    return REPO_DIR
