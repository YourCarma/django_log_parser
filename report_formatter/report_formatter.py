from collections import defaultdict
from datetime import datetime

class ReportFormatter:

    def group_by_count(self, group_object: list, objects_to_count: list, report_name: str = "handler"):
        print("Формирование отчета...")
        start_time = datetime.now()
        summary_stats = defaultdict(lambda: defaultdict(int))
        for route, status in zip(group_object, objects_to_count):
            summary_stats[route][status] += 1

        unique_objects_to_count = sorted(
                    {status
                    for counts in summary_stats.values()
                    for status in counts}  # Фильтруем None, если counts пуст
                )
        max_route_width = max(len(str(route)) for route in summary_stats) + 2
        if len(report_name) > max_route_width:
            max_route_width = len(report_name) + 2
        status_widths = {
            status: max(len(status), 5)
            for status in unique_objects_to_count
        }
        header = self.header(report_name, max_route_width,
                             unique_objects_to_count, status_widths)
        separator = self.separator(max_route_width, status_widths)
        print(separator)
        print(header)
        print(separator)
        for route in sorted(summary_stats):
            row = f"| {route:<{max_route_width}} |"
            for status in unique_objects_to_count:
                count = summary_stats[route].get(status, 0)
                row += f" {count:^{status_widths[status]}} |"
            print(row)
        print(separator)
        print(f"Всего объектов: {len(group_object)}")
        print(
            "Формирование отчета завершено\n"
            f"Время выполнения: {datetime.now() - start_time}"
        )

    def header(self, head_name: str, max_group_object_width: int,
               column_names: list[str], column_widths: dict[str, int]) -> str:
        """ ## Отрисовка шапки таблицы

        ### Args:
            `head_name` (str): Название таблицы
            `max_group_object_width` (int): Ширина названия таблицы, символы
            `column_names` (list[str]): Уникальный список имен колонок
            `column_widths` (dict[str, int]): Ширина колонок по именам таблицы

        Returns:
            str: Шапка таблицы формата\n
        ```
        |*head_name (Название таблицы)*| имя_колонки | имя_колонки  |...
        ```
        """
        header = f"| {f'{head_name}':^{max_group_object_width}} |"
        for name in column_names:
            header += f" {name:^{column_widths[name]}} |"
        return header

    def separator(self, max_group_object_width: int, column_widths: dict[str,
                                                                         int]):
        """ ## Отрисовка разделителя таблицы

        ### Args:
            `max_group_object_width` (str): Максимальная ширина объекта группировки, символы
            `column_widths` (dict[str, int]): Ширина названия таблицы, символы

        Returns:
            str: Разделитель таблицы\n
        ```
        +<---Ширина объекта группировки---->+<--колонка--->+<--колонка--->+
        ```
        """
        return "+" + "-" * (max_group_object_width + 2) + "+" + "+".join(
            ["-" * (w + 2) for w in column_widths.values()]) + "+"
