"""
Тесты для проверки 1-го урока Git.

Использует GitValidator для инспекции репозитория студента
в зависимости от выбранного уровня сложности.
"""

from pathlib import Path
from types import ModuleType
from core.models import DifficultyLevel, TestResult
from services.git_validator import GitValidator


def run_all_tests(student_module: ModuleType, level: DifficultyLevel) -> TestResult:
    """Запускает проверку репозитория студента по заданному уровню."""
    if not hasattr(student_module, "get_repo_path"):
        return TestResult(False, 1, 0, "В решении отсутствует функция get_repo_path()")

    repo_path: Path = student_module.get_repo_path()
    validator = GitValidator()

    if level == DifficultyLevel.BASE:
        return _test_base_level(validator, repo_path)
    elif level == DifficultyLevel.STANDARD:
        return _test_standard_level(validator, repo_path)
    return _test_advanced_level(validator, repo_path)


def _test_base_level(validator: GitValidator, repo_path: Path) -> TestResult:
    """Проверяет начальный репозиторий: .git и хотя бы 1 коммит с README."""
    if not (repo_path / ".git").is_dir():
        return TestResult(False, 2, 0, f"Директория {repo_path} не инициализирована как git (нет .git)")
    has_readme = (repo_path / "README.md").is_file()
    commits = validator._run_git_cmd(repo_path, ["rev-list", "--count", "HEAD"])
    commit_cnt = int(commits) if commits.isdigit() else 0
    passed = sum([commit_cnt >= 1, has_readme])
    return TestResult(passed == 2, 2, passed, f"Коммитов: {commit_cnt}/1, README: {has_readme}")


def _test_standard_level(validator: GitValidator, repo_path: Path) -> TestResult:
    """Проверяет стандартные требования методички СПбГУПТД."""
    return validator.validate_basics(repo_path)


def _test_advanced_level(validator: GitValidator, repo_path: Path) -> TestResult:
    """Проверяет продвинутые требования: .gitignore и от 4 коммитов."""
    base_res = validator.validate_basics(repo_path)
    if not base_res.success:
        return base_res
    has_gitignore = (repo_path / ".gitignore").is_file()
    commits = validator._run_git_cmd(repo_path, ["rev-list", "--count", "HEAD"])
    commit_cnt = int(commits) if commits.isdigit() else 0
    passed = base_res.passed_tests + int(has_gitignore) + int(commit_cnt >= 4)
    success = has_gitignore and (commit_cnt >= 4)
    return TestResult(success, 6, passed, f"{base_res.message}, .gitignore: {has_gitignore}, коммитов: {commit_cnt}/4")
