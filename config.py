"""
Конфигурация обучающего тренажёра.

Определяет:
  1. Пути к директориям уроков и документации
  2. Цветовые схемы ANSI для терминала
  3. Константы уровней сложности и параметров тестирования
"""

from dataclasses import dataclass
from pathlib import Path


# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent

# Директория с уроками
LESSONS_DIR = BASE_DIR / "lessons"

# Директория документации
DOCS_DIR = BASE_DIR / "docs"


@dataclass(frozen=True)
class TerminalColors:
    """Цветовые коды ANSI для форматирования консольного вывода."""
    RESET: str = "\033[0m"
    BOLD: str = "\033[1m"
    DIM: str = "\033[2m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    BLUE: str = "\033[94m"
    MAGENTA: str = "\033[95m"
    CYAN: str = "\033[96m"
    RED: str = "\033[91m"


COLORS = TerminalColors()
