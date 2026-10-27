"""
Урок 06: Бинарный поиск (Уровень 2: Стандарт кафедры ЦАТ).

Практическая работа: поиск числа x в диапазоне [a; b] без создания списка.
"""

import math
from typing import Any, Dict, List


def calculate_max_steps(a: int, b: int) -> int:
    """
    Вычисляет теоретический максимум шагов: ⌈log₂(n + 1)⌉, где n = b - a + 1.
    """
    n = b - a + 1
    return math.ceil(math.log2(n + 1))


def binary_search_range(a: int, b: int, x: int) -> Dict[str, Any]:
    """
    Выполняет бинарный поиск числа x в диапазоне [a; b].

    Валидация:
      - Если a > b, выбрасывает ValueError("Нижняя граница больше верхней").
      - Если x < a или x > b, выбрасывает ValueError("Число вне диапазона").

    Возвращает словарь:
      {
        "found": True/False,
        "steps": int,
        "max_theoretical_steps": int,
        "log": List[str]  # записи шагов: "Шаг 1: left=..., right=..., mid=..."
      }
    """
    # TODO: Реализуйте поиск по границам left, right без создания списка чисел
    pass
