import re
from pathlib import Path
from typing import Optional
from datetime import datetime
from log_parser.abstract_parser import AbstractLogParser


class DjangoRequestLogParser(AbstractLogParser):

    def __init__(self):
        self.LOG_TYPE_TEMPLATE = re.compile(r"django.request")
        self.METHODS = re.compile(r"\b(GET|POST|DELETE|PUT|PATCH|UPDATE)\b")
        self.LOGGER_STATUSES = re.compile(
            r"\b(INFO|CRITICAL|WARNING|DEBUG|ERROR)\b")
        self.SOURCE = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")
        self.DATETIME = re.compile(
            r"\b(\d{1,4}\-\d{1,2}\-\d{1,2}\s\d{1,2}\:\d{1,2}:\d{1,2})")
        self.ROUTES = re.compile(r"(\/[^\s]+)")
        self.RESPONSE = re.compile(r"\s\d{3}\s")

    def get_file_lines(self, filepath: Path) -> list[str]:
        """## Получение всех строк файла логов
        ### Args:
            `filepath` (Path): Пусть к файлу

        ### Returns:
            `list`: Список логов из файла
        """
        with open(filepath, 'r') as file:
            logs = file.readlines()
        return logs

    def log_type_check(self, logs: list[str]) -> list[str]:
        """## Фильтрация определенного типа логов
        Фильрует **исходный список логов** по определенному **типу** логов - данном классе `django.request`

        ### Args:
            `logs` (list): *Исходный список логов*

        ### Returns:
            `list`: *Отфильтрованный список логов*
        """
        return list(
            filter(lambda x: bool(re.search(self.LOG_TYPE_TEMPLATE, x)), logs))

    def extract_pattern(self, log: str,
                        target_object: re.Pattern) -> Optional[str]:
        """## Извлечение шаблона из текста

        ### Args:
            `log` (str): один объект лога
            `target_object` (re.Pattern): шаблон регулярного выражения

        ### Returns:
            `Optional[str]`: Найденная строка или `None`
        """
        matched_object = re.search(target_object, log)
        if not matched_object:
            return str(None)
        return matched_object.group().strip()

    def get_logger_statuses(self, logs: list[str]) -> list[Optional[str]]:
        """## Извлечение статусов логгера
        ### На основе шаблона `self.LOGGER_STATUSES`
        ### Args:
            `logs` (list): Отфильтрованный список логов

        ### Returns:
            `list`: Список статусов логгера
        """
        return [
            self.extract_pattern(log, self.LOGGER_STATUSES) for log in logs
        ]

    def get_method(self, logs: list[str]) -> list[Optional[str]]:
        """## Извлечение REST-методов
        ### На основе шаблона `self.METHODS`
        ### Args:
            `logs` (list): Отфильтрованный список логов

        ### Returns:
            `list`: Список REST-методов
        """
        return [self.extract_pattern(log, self.METHODS) for log in logs]

    def get_source_ip(self, logs: list[str]) -> list[Optional[str]]:
        """## Извлечение IPv4 источника
        ### На основе шаблона `self.SOURCE`
        ### Args:
            `logs` (list): Отфильтрованный список логов

        ### Returns:
            `list`: Список IPv4 источника
        """
        return [self.extract_pattern(log, self.SOURCE) for log in logs]

    def get_datetime(self, logs: list[str]) -> list[Optional[str]]:
        """## Извлечение `datetime` логов
        ### На основе шаблона `self.DATETIME`
        ### Args:
            `logs` (list): Отфильтрованный список логов

        ### Returns:
            `list`: Список `datetime` логов
        """
        return [self.extract_pattern(log, self.DATETIME) for log in logs]

    def get_routes(self, logs: list[str]) -> list[Optional[str]]:
        """## Извлечение ручек (URL) запроса
        ### На основе шаблона `self.ROUTES`
        ### Args:
            `logs` (list): Отфильтрованный список логов

        ### Returns:
            `list`: Список ручек запроса
        """
        return [self.extract_pattern(log, self.ROUTES) for log in logs]

    def get_responses(self, logs: list[str]) -> list[Optional[str]]:
        """## Извлечение HTTP-статуса ответа сервера
        ### На основе шаблона `self.RESPONSE`
        ### Args:
            `logs` (list): Отфильтрованный список логов

        ### Returns:
            `list`: Список HTTP-статуса ответа сервера
        """
        return [self.extract_pattern(log, self.RESPONSE) for log in logs]
    
    def parse(self, filepath: Path) -> dict[str, list[Optional[str]]]:
        """## Алгоритм парсинга и поиска шаблонов в логах
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
        print(f"Парсинг файла: {filepath}")
        start_time = datetime.now()
        raw_logs = self.get_file_lines(filepath)
        filtered_logs = self.log_type_check(raw_logs)
        logger_statuses = self.get_logger_statuses(filtered_logs)
        methods = self.get_method(filtered_logs)
        sources = self.get_source_ip(filtered_logs)
        log_datetime = self.get_datetime(filtered_logs)
        routes = self.get_routes(filtered_logs)
        responses = self.get_responses(filtered_logs)
        structured_logs = {
            "logger_statuses": logger_statuses,
            "methods": methods,
            "sources": sources,
            "datetime": log_datetime,
            "routes": routes,
            "responses": responses
        }
        print(
            f"Парсинг файла {filepath} завершен.\n"
            f"Время выполнения: {datetime.now() - start_time}"
        )
        return structured_logs
