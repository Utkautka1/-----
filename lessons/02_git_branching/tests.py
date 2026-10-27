"""
Тесты для проверки 2-го урока Git (ветвление и конфликты).

Проверяет создание ветки new, наличие коммита слияния и отсутствие
неразрешённых конфликтов.
"""

from pathlib import Path
from types import ModuleType
from core.models import DifficultyLevel, TestResult
from services.git_validator import GitValidator


def run_all_tests(student_module: ModuleType, level: DifficultyLevel) -> TestResult:
    """Запускает валидацию репозитория с ветвлением."""
    if not hasattr(student_module, "get_repo_path"):
        return TestResult(False, 1, 0, "Отсутствует функция get_repo_path()")

    repo_path: Path = student_module.get_repo_path()
    validator = GitValidator()

    if level == DifficultyLevel.BASE:
        return _test_base_branching(validator, repo_path)
    return validator.validate_branching(repo_path)


def _test_base_branching(validator: GitValidator, repo_path: Path) -> TestResult:
    """Проверяет базовое ветвление без обязательного конфликта."""
    if not (repo_path / ".git").is_dir():
        return TestResult(False, 2, 0, "Папка не является git-репозиторием")
    branches = validator._run_git_cmd(repo_path, ["branch", "-a"])
    has_new = "new" in branches
    commits = validator._run_git_cmd(repo_path, ["rev-list", "--count", "HEAD"])
    commit_cnt = int(commits) if commits.isdigit() else 0
    passed = sum([has_new, commit_cnt >= 2])
    return TestResult(passed == 2, 2, passed, f"Ветка new: {has_new}, Коммитов: {commit_cnt}/2")
