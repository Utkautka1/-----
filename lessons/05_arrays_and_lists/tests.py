"""
Тесты для проверки 5-го урока (массивы и списки).

Включает проверку модификации in-place и рандомизированное тестирование (Fuzzing).
"""

import random
from types import ModuleType
from core.models import DifficultyLevel, TestResult


def run_all_tests(student_module: ModuleType, level: DifficultyLevel) -> TestResult:
    """Запускает проверки для списков и массивов."""
    if level == DifficultyLevel.BASE:
        return _test_base(student_module)
    elif level == DifficultyLevel.STANDARD:
        return _test_standard(student_module)
    return _test_advanced(student_module)


def _test_base(mod: ModuleType) -> TestResult:
    """Проверяет ручной поиск суммы и максимума."""
    if not hasattr(mod, "find_list_sum") or not hasattr(mod, "find_list_max"):
        return TestResult(False, 1, 0, "Отсутствуют функции find_list_sum или find_list_max")

    passed = 0
    if mod.find_list_sum([1, 2, 3, 4, 5]) == 15:
        passed += 1
    if mod.find_list_sum([-10, 10, 5]) == 5:
        passed += 1
    if mod.find_list_max([3, 7, 2, 9, 1]) == 9:
        passed += 1
    if mod.find_list_max([-50, -10, -20]) == -10:
        passed += 1
    return TestResult(passed == 4, 4, passed, f"Пройдено тестов: {passed}/4")


def _test_standard(mod: ModuleType) -> TestResult:
    """Проверяет разворот списка in-place и удаление дубликатов."""
    if not hasattr(mod, "reverse_list_inplace") or not hasattr(mod, "remove_duplicates_ordered"):
        return TestResult(False, 1, 0, "Отсутствуют обязательные функции")

    passed = _check_in_place_reverse(mod) + _check_duplicates(mod)
    total = 12
    return TestResult(passed == total, total, passed, f"Стандартных тестов пройдено: {passed}/{total}")


def _check_in_place_reverse(mod: ModuleType) -> int:
    """Проверяет разворот на 10 случайных списках."""
    passed = 0
    rng = random.Random(777)
    for _ in range(10):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(2, 20))]
        expected = list(reversed(arr))
        mod.reverse_list_inplace(arr)
        if arr == expected:
            passed += 1
    return passed


def _check_duplicates(mod: ModuleType) -> int:
    """Проверяет сохранение порядка при удалении дубликатов."""
    passed = 0
    t1 = mod.remove_duplicates_ordered([1, 2, 2, 3, 1, 4])
    if t1 == [1, 2, 3, 4]:
        passed += 1
    t2 = mod.remove_duplicates_ordered([5, 5, 5, 5])
    if t2 == [5]:
        passed += 1
    return passed


def _test_advanced(mod: ModuleType) -> TestResult:
    """Проверяет слияние отсортированных списков на случайных данных."""
    if not hasattr(mod, "merge_sorted_lists"):
        return TestResult(False, 1, 0, "Отсутствует merge_sorted_lists")
    passed = 0
    rng = random.Random(999)
    for _ in range(5):
        a = sorted([rng.randint(0, 100) for _ in range(rng.randint(1, 10))])
        b = sorted([rng.randint(0, 100) for _ in range(rng.randint(1, 10))])
        expected = sorted(a + b)
        if mod.merge_sorted_lists(a, b) == expected:
            passed += 1
    return TestResult(passed == 5, 5, passed, f"Продвинутых тестов: {passed}/5")
