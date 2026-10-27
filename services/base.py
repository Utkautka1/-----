"""
Базовый класс для всех сервисов системы.

Определяет общий логгер и интерфейсы жизненного цикла сервисов.
"""

from abc import ABC
from core.logger import get_logger


class BaseService(ABC):
    """Абстрактный класс сервиса с преднастроенным логгером."""

    def __init__(self, service_name: str) -> None:
        # service_name — смысловой идентификатор подсистемы для роутинга логов
        self.log = get_logger(service_name)
