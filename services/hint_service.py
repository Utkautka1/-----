"""
Сервис ступенчатых подсказок (Progressive Disclosure).

Позволяет студентам получать помощь дозированно:
  1. Уровень 1: Идея и наводящие вопросы
  2. Уровень 2: Алгоритм и псевдокод
  3. Уровень 3: Полный эталонный разбор кода
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from core.models import Hint
from services.base import BaseService


class HintService(BaseService):
    """Управляет загрузкой и форматированием подсказок к урокам."""

    def __init__(self) -> None:
        super().__init__("hint_service")

    def load_hints(self, hints_file: Path) -> List[Hint]:
        """Загружает подсказки из JSON-файла урока."""
        if not hints_file.exists():
            self.log.warning(f"Файл подсказок не найден: {hints_file}")
            return []
        try:
            with open(hints_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Hint(h["level"], h["title"], h["content"]) for h in data]
        except Exception as e:
            self.log.error(f"Ошибка парсинга подсказок {hints_file}: {e}")
            return []

    def get_hint_by_level(self, hints: List[Hint], level: int) -> Optional[Hint]:
        """Возвращает подсказку конкретного уровня (1, 2 или 3)."""
        for hint in hints:
            if hint.level == level:
                return hint
        return None

    def format_hint(self, hint: Hint) -> str:
        """Форматирует подсказку для вывода в консоль."""
        level_icons = {1: "💡 [Уровень 1: Идея]", 2: "📐 [Уровень 2: Алгоритм]", 3: "💻 [Уровень 3: Код и Разбор]"}
        header = level_icons.get(hint.level, f"[Уровень {hint.level}]")
        lines = [
            "=" * 60,
            f"{header} {hint.title}",
            "=" * 60,
            hint.content,
            "=" * 60,
        ]
        return "\n".join(lines)
