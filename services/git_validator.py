"""
Валидатор практических заданий по Git.

Проверяет реальное состояние локального Git-репозитория студента:
наличие веток, количество коммитов, слияния, разрешение конфликтов.
"""

import subprocess
from pathlib import Path
from core.models import TestResult
from services.base import BaseService


class GitValidator(BaseService):
    """Инспектирует Git-репозиторий студента через команды git CLI."""

    def __init__(self) -> None:
        super().__init__("git_validator")

    def _run_git_cmd(self, repo_dir: Path, args: list) -> str:
        """Выполняет команду git в директории репозитория и возвращает stdout."""
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            return res.stdout.strip()
        except Exception as e:
            self.log.debug(f"Git cmd failed {args}: {e}")
            return ""

    def validate_basics(self, repo_dir: Path) -> TestResult:
        """Проверяет выполнение практики 'Git начало'."""
        if not (repo_dir / ".git").is_dir():
            return TestResult(False, 4, 0, f"Папка {repo_dir.name} не является git-репозиторием (нет .git)")
        commits = self._run_git_cmd(repo_dir, ["rev-list", "--count", "HEAD"])
        commit_count = int(commits) if commits.isdigit() else 0
        has_readme = (repo_dir / "README.md").is_file()
        has_diff = (repo_dir / "diff.txt").is_file()
        has_log = (repo_dir / "log.txt").is_file()

        passed = sum([commit_count >= 3, has_readme, has_diff, has_log])
        msg = f"Коммитов: {commit_count}/3, README: {has_readme}, diff.txt: {has_diff}, log.txt: {has_log}"
        return TestResult(passed == 4, 4, passed, msg)

    def validate_branching(self, repo_dir: Path) -> TestResult:
        """Проверяет выполнение практики 'Git ветвление' со слиянием."""
        if not (repo_dir / ".git").is_dir():
            return TestResult(False, 3, 0, "Репозиторий не найден")
        log_graph = self._run_git_cmd(repo_dir, ["log", "--oneline", "--merges"])
        has_merge_commit = len(log_graph) > 0
        branches = self._run_git_cmd(repo_dir, ["branch", "-a"])
        has_new_branch = "new" in branches
        unmerged = self._run_git_cmd(repo_dir, ["diff", "--name-only", "--diff-filter=U"])
        no_conflicts_left = len(unmerged) == 0

        passed = sum([has_new_branch, has_merge_commit, no_conflicts_left])
        msg = f"Ветка new создана: {has_new_branch}, Слияние выполнено: {has_merge_commit}, Конфликт разрешен: {no_conflicts_left}"
        return TestResult(passed == 3, 3, passed, msg)
