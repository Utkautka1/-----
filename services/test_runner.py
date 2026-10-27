"""
Универсальный раннер тестов учебных заданий.

Запускает проверку решений студентов с поддержкой:
  1. Выбора уровня сложности (Новичок, Практик, Профи)
  2. Рандомизированного тестирования против списывания (Fuzzing)
  3. Перехвата ввода/вывода (mock sys.stdin/stdout)
  4. Дружелюбной расшифровки ошибок для новичков
"""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Optional
from core.models import DifficultyLevel, Lesson, TestResult
from services.base import BaseService


class TestRunner(BaseService):
    """Исполнитель тестов для упражнений по Python и практикам."""

    def __init__(self) -> None:
        super().__init__("test_runner")

    def run_tests(self, lesson: Lesson, level: DifficultyLevel) -> TestResult:
        """Запускает набор тестов для указанного урока и уровня сложности."""
        tests_file = lesson.path / "tests.py"
        if not tests_file.exists():
            return TestResult(False, 0, 0, f"Файл тестов {tests_file.name} не найден")

        exercise_file = lesson.path / f"exercise_{level.value}.py"
        if not exercise_file.exists():
            return TestResult(False, 0, 0, f"Файл решения {exercise_file.name} не найден")

        return self._execute_test_suite(tests_file, exercise_file, level)

    def _execute_test_suite(self, tests_file: Path, exercise_file: Path, level: DifficultyLevel) -> TestResult:
        """Импортирует решение студента и вызывает функцию проверки из tests.py."""
        student_module = self._import_module_from_path("student_solution", exercise_file)
        if not student_module:
            return TestResult(False, 1, 0, "Синтаксическая ошибка в вашем коде. Проверьте отступы и скобки!")

        test_module = self._import_module_from_path("lesson_tests", tests_file)
        if not test_module or not hasattr(test_module, "run_all_tests"):
            return TestResult(False, 1, 0, "Ошибка в модуле тестов: отсутствует run_all_tests")

        try:
            return test_module.run_all_tests(student_module, level)
        except Exception as e:
            self.log.error(f"Необработанное исключение при тестировании: {e}")
            return TestResult(False, 1, 0, f"Ошибка выполнения: {e}")

    def _import_module_from_path(self, module_name: str, file_path: Path) -> Optional[ModuleType]:
        """Динамически импортирует Python-файл как модуль."""
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader:
                return None
            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)
            return mod
        except Exception as e:
            self.log.warning(f"Ошибка загрузки модуля {file_path.name}: {e}")
            return None
