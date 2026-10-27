"""
Тесты для проверки 4-го урока (алгоритмы и блок-схемы).

Проверяет правильность трассировки алгоритмов, циклов и расчёта сложности.
"""

from types import ModuleType
from core.models import DifficultyLevel, TestResult


def run_all_tests(student_module: ModuleType, level: DifficultyLevel) -> TestResult:
    """Запускает проверку алгоритмов по выбранному уровню."""
    if level == DifficultyLevel.BASE:
        return _test_base(student_module)
    elif level == DifficultyLevel.STANDARD:
        return _test_standard(student_module)
    return _test_advanced(student_module)


def _test_base(mod: ModuleType) -> TestResult:
    """Проверяет базовую линейную трассировку."""
    if not hasattr(mod, "trace_linear_algorithm"):
        return TestResult(False, 1, 0, "Отсутствует функция trace_linear_algorithm")
    passed = 0
    # x=2, y=3 -> x=7, y=6 -> result=13
    if mod.trace_linear_algorithm(2, 3) == 13:
        passed += 1
    # x=10, y=5 -> x=15, y=10 -> result=25
    if mod.trace_linear_algorithm(10, 5) == 25:
        passed += 1
    return TestResult(passed == 2, 2, passed, f"Пройдено тестов: {passed}/2")


def _test_standard(mod: ModuleType) -> TestResult:
    """Проверяет трассировку цикла Сиракуз (3n+1) и цикломатическую сложность."""
    if not hasattr(mod, "trace_loop_with_branching") or not hasattr(mod, "calculate_cyclomatic_complexity"):
        return TestResult(False, 1, 0, "Отсутствуют обязательные функции")
    passed = 0
    # Для n=6: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 (8 шагов)
    if mod.trace_loop_with_branching(6) == 8:
        passed += 1
    # Для n=1: 0 шагов
    if mod.trace_loop_with_branching(1) == 0:
        passed += 1
    # Сложность: P=3 -> V=4
    if mod.calculate_cyclomatic_complexity(3) == 4:
        passed += 1
    return TestResult(passed == 3, 3, passed, f"Стандартных тестов пройдено: {passed}/3")


def _test_advanced(mod: ModuleType) -> TestResult:
    """Проверяет детектор зацикливания."""
    if not hasattr(mod, "will_loop_terminate"):
        return TestResult(False, 1, 0, "Отсутствует will_loop_terminate")
    passed = 0
    # start=0, step=2, limit=10 -> достижимо (True)
    if mod.will_loop_terminate(0, 2, 10) is True:
        passed += 1
    # start=0, step=2, limit=9 -> перескочит (False)
    if mod.will_loop_terminate(0, 2, 9) is False:
        passed += 1
    # start=10, step=2, limit=0 -> уйдёт в плюс бесконечность (False)
    if mod.will_loop_terminate(10, 2, 0) is False:
        passed += 1
    return TestResult(passed == 3, 3, passed, f"Продвинутых тестов: {passed}/3")
