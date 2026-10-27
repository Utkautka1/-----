"""
Сервис управления каталогом уроков.

Сканирует директорию `lessons/`, формирует список доступных уроков
и предоставляет доступ к файлам упражнений по выбранному уровню сложности.
"""

from pathlib import Path
from typing import List, Optional
from config import LESSONS_DIR
from core.models import DifficultyLevel, Lesson
from services.base import BaseService


class LessonService(BaseService):
    """Сервис для обнаружения, чтения метаданных и выдачи файлов уроков."""

    def __init__(self, lessons_root: Path = LESSONS_DIR) -> None:
        super().__init__("lesson_service")
        self.lessons_root = lessons_root

    def get_all_lessons(self) -> List[Lesson]:
        """Возвращает отсортированный список всех найденных уроков."""
        if not self.lessons_root.exists():
            return []
        lessons = []
        for folder in sorted(self.lessons_root.iterdir()):
            if folder.is_dir() and folder.name.startswith(("0", "1", "2")):
                lesson = self._parse_lesson_folder(folder)
                if lesson:
                    lessons.append(lesson)
        return lessons

    def _parse_lesson_folder(self, folder: Path) -> Optional[Lesson]:
        """Парсит имя папки вида 01_git_basics и возвращает объект Lesson."""
        parts = folder.name.split("_", 1)
        if not parts[0].isdigit():
            return None
        idx = int(parts[0])
        slug = parts[1] if len(parts) > 1 else ""
        title = self._read_title_from_readme(folder) or slug.replace("_", " ").title()
        return Lesson(
            index=idx,
            slug=slug,
            title=title,
            path=folder,
            description=f"Урок {idx}: {title}",
        )

    def _read_title_from_readme(self, folder: Path) -> Optional[str]:
        """Извлекает первый заголовок H1 из README.md урока."""
        readme = folder / "README.md"
        if not readme.exists():
            return None
        with open(readme, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("# "):
                    return stripped[2:].strip()
        return None

    def get_lesson_by_index(self, index: int) -> Optional[Lesson]:
        """Ищет урок по его порядковому номеру."""
        for lesson in self.get_all_lessons():
            if lesson.index == index:
                return lesson
        return None

    def get_exercise_file(self, lesson: Lesson, level: DifficultyLevel) -> Path:
        """Возвращает путь к файлу с упражнением заданного уровня сложности."""
        return lesson.path / f"exercise_{level.value}.py"

    def get_hints_file(self, lesson: Lesson) -> Path:
        """Возвращает путь к файлу подсказок урока."""
        return lesson.path / "hints.json"

    def get_quiz_file(self, lesson: Lesson) -> Path:
        """Возвращает путь к файлу проверочных вопросов урока."""
        return lesson.path / "quiz.json"
