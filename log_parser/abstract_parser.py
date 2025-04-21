from abc import ABC, abstractmethod
from pathlib import Path


class AbstractLogParser(ABC):

    def __init__(self):
        self.LOG_TYPE_TEMPLATE = ...

    @abstractmethod
    def get_file_lines(self, filepath: Path) -> list[str]:
        """## Получение всех строк файла логов
        ### Args:
            `filepath` (Path): Пусть к файлу

        ### Returns:
            `list`: Список логов из файла
        """
        pass

    @abstractmethod
    def parse(self):
        """## Общий алгоритм структурирования логов
        ### Args:
            `filepath` (Path): Путь к файлу логов

        ### Returns:
            `dict`: Словарь всех типов событий логов в формате:
            ```json
            {
                `logger_statuses`: ["ERROR", ...],
                `methods`: ["GET", "PUT", ...],
                `sources`: ["192.168.0.1", ...],
                `datetime`: ["2025-03-28 12:11:57", ...],
                `routes`: ["/admin/dashboard/", ...],
                `responses`: ["201", ...]
            }
            ```
        ! Все списки объектов одинаковой длины, означающей, что индекс каждого списка явялется одной записью лога
        """
        pass
