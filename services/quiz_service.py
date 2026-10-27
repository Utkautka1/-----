"""
Сервис интерактивного тестирования понимания (Quiz Engine).

Проверяет, действительно ли студент понял работу алгоритма,
а не просто скопировал решение из подсказки или у одногруппника.
"""

import json
from pathlib import Path
from typing import List
from config import COLORS
from core.models import QuizQuestion
from services.base import BaseService


class QuizService(BaseService):
    """Проводит интерактивный квиз по материалам урока в консоли."""

    def __init__(self) -> None:
        super().__init__("quiz_service")

    def load_quiz(self, quiz_file: Path) -> List[QuizQuestion]:
        """Загружает вопросы квиза из JSON-файла урока."""
        if not quiz_file.exists():
            return []
        try:
            with open(quiz_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [
                QuizQuestion(
                    q["question"], q["options"], q["correct_idx"], q["explanation"]
                )
                for q in data
            ]
        except Exception as e:
            self.log.error(f"Ошибка чтения квиза {quiz_file}: {e}")
            return []

    def ask_question(self, index: int, q: QuizQuestion) -> bool:
        """Задает один вопрос, принимает ответ пользователя и выводит разбор."""
        print(f"\n{COLORS.BOLD}Вопрос {index}: {q.question}{COLORS.RESET}")
        for i, opt in enumerate(q.options, start=1):
            print(f"  [{i}] {opt}")
        choice = self._get_valid_input(len(q.options))
        is_correct = (choice - 1) == q.correct_idx
        self._display_feedback(is_correct, q.explanation)
        return is_correct

    def _get_valid_input(self, max_options: int) -> int:
        """Запрашивает число от 1 до max_options с валидацией ввода."""
        while True:
            raw = input(f"{COLORS.CYAN}Ваш ответ (1-{max_options}): {COLORS.RESET}").strip()
            if raw.isdigit() and 1 <= int(raw) <= max_options:
                return int(raw)
            print(f"{COLORS.RED}Пожалуйста, введите число от 1 до {max_options}{COLORS.RESET}")

    def _display_feedback(self, is_correct: bool, explanation: str) -> None:
        """Выводит вердикт и объяснение ответа."""
        if is_correct:
            print(f"{COLORS.GREEN}✅ Верно!{COLORS.RESET}")
        else:
            print(f"{COLORS.RED}❌ Неверно.{COLORS.RESET}")
        print(f"{COLORS.DIM}Объяснение: {explanation}{COLORS.RESET}")
