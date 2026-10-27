"""
Тесты для проверки 3-го урока Python (условия и валидация).

Включает детерминированные проверки краевых случаев (1900, 2000)
и рандомизированное тестирование (Fuzzing) на случайных числах.
"""

import math
import random
from types import ModuleType
from core.models import DifficultyLevel, TestResult


def run_all_tests(student_module: ModuleType, level: DifficultyLevel) -> TestResult:
    """Запускает тестирование по выбранному уровню сложности."""
    if level == DifficultyLevel.BASE:
        return _test_base(student_module)
    elif level == DifficultyLevel.STANDARD:
        return _test_standard(student_module)
    return _test_advanced(student_module)


def _test_base(mod: ModuleType) -> TestResult:
    """Проверяет базовые функции високосного года и прямоугольника."""
    if not hasattr(mod, "is_leap_year") or not hasattr(mod, "calculate_rectangle_area"):
        return TestResult(False, 1, 0, "Отсутствуют функции is_leap_year или calculate_rectangle_area")

    passed = 0
    total = 5
    if mod.is_leap_year(2024) is True and mod.is_leap_year(1900) is False:
        passed += 2
    if mod.is_leap_year(2000) is True:
        passed += 1

    r_area = mod.calculate_rectangle_area(5.0, 4.0)
    if isinstance(r_area, (int, float)) and abs(r_area - 20.0) < 1e-5:
        passed += 1

    c_area = mod.calculate_circle_area(3.0) if hasattr(mod, "calculate_circle_area") else None
    if isinstance(c_area, (int, float)) and abs(c_area - (math.pi * 9.0)) < 1e-4:
        passed += 1

    msg = f"Пройдено тестов: {passed}/{total}"
    if passed == 0:
        msg += " (Функции пока возвращают None — заполните решения в файле)"
    return TestResult(passed == total, total, passed, msg)


def _test_standard(mod: ModuleType) -> TestResult:
    """Проверяет стандартные требования методички с рандомизацией."""
    req_funcs = ["validate_year_string", "is_leap_year", "calculate_triangle_heron"]
    for fn in req_funcs:
        if not hasattr(mod, fn):
            return TestResult(False, 1, 0, f"Отсутствует обязательная функция {fn}")

    passed = _check_year_validation(mod) + _check_leap_fuzzing(mod) + _check_heron_triangle(mod)
    total = 20
    msg = f"Стандартных тестов пройдено: {passed}/{total}"
    if passed == 0:
        msg += " (Функции возвращают None — реализуйте решения по заданию)"
    return TestResult(passed == total, total, passed, msg)


def _check_year_validation(mod: ModuleType) -> int:
    """Проверяет корректность валидации строки года."""
    cases = [("2024", True), ("1900", True), ("999", False), ("10000", False), ("20a4", False)]
    passed = 0
    for text, expected in cases:
        res = mod.validate_year_string(text)
        if res is expected:
            passed += 1
    return passed


def _check_leap_fuzzing(mod: ModuleType) -> int:
    """Запускает рандомизированные тесты на високосный год."""
    passed = 0
    rng = random.Random(42)
    for _ in range(10):
        y = rng.randint(1000, 3000)
        expected = (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
        if mod.is_leap_year(y) == expected:
            passed += 1
    return passed


def _check_heron_triangle(mod: ModuleType) -> int:
    """Проверяет формулу Герона и обработку несуществующих треугольников."""
    passed = 0
    res = mod.calculate_triangle_heron(3.0, 4.0, 5.0)
    if isinstance(res, (int, float)) and abs(res - 6.0) < 1e-5:
        passed += 2
    try:
        mod.calculate_triangle_heron(1.0, 2.0, 10.0)
    except ValueError:
        passed += 3
    return passed


def _test_advanced(mod: ModuleType) -> TestResult:
    """Проверяет продвинутый парсер и строгое неравенство."""
    if not hasattr(mod, "parse_positive_number"):
        return TestResult(False, 1, 0, "Отсутствует функция parse_positive_number")
    passed = 0
    r1 = mod.parse_positive_number(" 2,5 ")
    if isinstance(r1, (int, float)) and abs(r1 - 2.5) < 1e-5:
        passed += 1
    r2 = mod.parse_positive_number("10.0")
    if isinstance(r2, (int, float)) and abs(r2 - 10.0) < 1e-5:
        passed += 1
    try:
        mod.parse_positive_number("-5")
    except ValueError:
        passed += 1
    return TestResult(passed == 3, 3, passed, f"Продвинутых тестов: {passed}/3")
