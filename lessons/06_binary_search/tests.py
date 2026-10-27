"""
Тесты для 6-го урока по бинарному поиску.

Проверяет все сценарии из таблицы методички кафедры ЦАТ СПбГУПТД:
краевые границы, отрицательные диапазоны, большие числа и валидацию.
"""

from types import ModuleType
from core.models import DifficultyLevel, TestResult


def run_all_tests(student_module: ModuleType, level: DifficultyLevel) -> TestResult:
    """Запускает тестирование бинарного поиска."""
    if level == DifficultyLevel.BASE:
        return _test_base(student_module)
    elif level == DifficultyLevel.STANDARD:
        return _test_standard(student_module)
    return _test_advanced(student_module)


def _test_base(mod: ModuleType) -> TestResult:
    """Проверяет классический бинарный поиск в списке."""
    if not hasattr(mod, "binary_search_array"):
        return TestResult(False, 1, 0, "Отсутствует функция binary_search_array")
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    passed = 0
    if mod.binary_search_array(arr, 23) == 5:
        passed += 1
    if mod.binary_search_array(arr, 2) == 0:
        passed += 1
    if mod.binary_search_array(arr, 91) == 9:
        passed += 1
    if mod.binary_search_array(arr, 999) == -1:
        passed += 1
    return TestResult(passed == 4, 4, passed, f"Базовых тестов: {passed}/4")


def _test_standard(mod: ModuleType) -> TestResult:
    """Проверяет практическую работу СПбГУПТД по тестовым наборам."""
    if not hasattr(mod, "binary_search_range") or not hasattr(mod, "calculate_max_steps"):
        return TestResult(False, 1, 0, "Отсутствуют обязательные функции")
    passed = _check_spbguptd_cases(mod) + _check_error_cases(mod)
    total = 8
    msg = f"Университетских тестов пройдено: {passed}/{total}"
    if passed == 0:
        msg += " (Функция возвращает None — напишите реализацию в exercise_standard.py)"
    return TestResult(passed == total, total, passed, msg)


def _check_spbguptd_cases(mod: ModuleType) -> int:
    """Проверяет 6 корректных сценариев из Таблицы 3 методички."""
    test_cases = [
        (1, 100, 73, 7), (1, 100, 1, 7), (1, 100, 100, 7),
        (5, 5, 5, 1), (-50, 50, -17, 7), (1, 1000000, 999999, 20)
    ]
    passed = 0
    for a, b, x, max_allowed in test_cases:
        res = mod.binary_search_range(a, b, x)
        if not isinstance(res, dict):
            continue
        is_ok = res.get("found") is True and res.get("steps", 999) <= max_allowed
        has_log = len(res.get("log", [])) > 0
        if is_ok and has_log:
            passed += 1
    return passed


def _check_error_cases(mod: ModuleType) -> int:
    """Проверяет ситуации ошибок ввода (a > b и x вне диапазона)."""
    passed = 0
    try:
        mod.binary_search_range(100, 1, 50)
    except ValueError:
        passed += 1
    try:
        mod.binary_search_range(1, 10, 25)
    except ValueError:
        passed += 1
    return passed


def _test_advanced(mod: ModuleType) -> TestResult:
    """Проверяет рекурсивный поиск и игру 'Угадай число'."""
    if not hasattr(mod, "binary_search_recursive") or not hasattr(mod, "play_guess_number"):
        return TestResult(False, 1, 0, "Отсутствуют продвинутые функции")
    passed = 0
    steps = mod.binary_search_recursive(1, 100, 73)
    if isinstance(steps, int) and 1 <= steps <= 7:
        passed += 1
    secret = 42
    judge = lambda mid: "угадал" if mid == secret else ("меньше" if secret < mid else "больше")
    if mod.play_guess_number(1, 100, judge) == secret:
        passed += 1
    return TestResult(passed == 2, 2, passed, f"Продвинутых тестов: {passed}/2")
