"""
Модели данных предметной области тренажёра.

Определяет:
  1. Перечисление уровней сложности (Новичок, Практик, Профи)
  2. Структуры уроков, заданий, тестов, подсказок и персональных вариантов
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class DifficultyLevel(str, Enum):
    """Уровни сложности учебных заданий."""
    BASE = "base"          # С нуля: базовый синтаксис, аналогии, подсказки
    STANDARD = "standard"  # Стандарт: 
    ADVANCED = "advanced"  # Профи: оптимизация, краевые случаи, бонусы


@dataclass
class Hint:
    """Трёхуровневая подсказка к заданию."""
    level: int             # 1 = идея, 2 = алгоритм, 3 = эталонный код
    title: str             # Название этапа подсказки
    content: str           # Текст подсказки или код с пояснением


@dataclass
class QuizQuestion:
    """Контрольный вопрос для проверки понимания темы."""
    question: str
    options: List[str]
    correct_idx: int
    explanation: str


@dataclass
class TestResult:
    """Результат выполнения проверки кода студента."""
    success: bool
    total_tests: int
    passed_tests: int
    message: str
    diff_details: Optional[str] = None


@dataclass
class Lesson:
    """Учебный модуль (урок)."""
    index: int
    slug: str
    title: str
    path: Path
    description: str
    available_levels: List[DifficultyLevel] = field(
        default_factory=lambda: [
            DifficultyLevel.BASE,
            DifficultyLevel.STANDARD,
            DifficultyLevel.ADVANCED,
        ]
    )
