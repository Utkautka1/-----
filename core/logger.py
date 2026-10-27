"""
Модуль структурированного логирования тренажёра.

Обеспечивает единый формат логирования с цветовой индикацией уровней
для отладки прогона тестов и фиксации действий студента.
"""

import logging
import sys
from config import COLORS


class ColoredFormatter(logging.Formatter):
    """Форматировщик логов с ANSI-раскраской в зависимости от уровня."""

    LEVEL_COLORS = {
        logging.DEBUG: COLORS.DIM,
        logging.INFO: COLORS.CYAN,
        logging.WARNING: COLORS.YELLOW,
        logging.ERROR: COLORS.RED,
        logging.CRITICAL: COLORS.RED + COLORS.BOLD,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Раскрашивает префикс лога в цвет соответствующего уровня."""
        color = self.LEVEL_COLORS.get(record.levelno, COLORS.RESET)
        prefix = f"{color}[{record.levelname}]{COLORS.RESET}"
        return f"{prefix} {record.getMessage()}"


def get_logger(name: str = "tutor") -> logging.Logger:
    """
    Возвращает настроенный логгер с потоковым выводом в stderr.

    Используем кастомный форматтер для наглядности при прогоне тестов.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(ColoredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
