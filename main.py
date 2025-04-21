import argparse
from pathlib import Path
from datetime import datetime

from log_parser.parser import DjangoRequestLogParser
from report_formatter.report_formatter import ReportFormatter
from utils import check_file_exist, combine_dicts


def main(filenames: list[str], report_name: str = "Handler"):
    existing_files = [
        Path(file_name) for file_name in filenames
        if check_file_exist(Path(file_name))
    ]
    if not existing_files:
        print("На вход отсутсвуют файлы. Завершение программы...")
        exit()

    log_parser = DjangoRequestLogParser()
    report_formatter = ReportFormatter()
    structured_logs = [
        log_parser.parse(file_name) for file_name in existing_files
    ]
    combined_logs = combine_dicts(structured_logs)
    
    # Здесь задаются объекты группировки для отчета
    group_by_object = combined_logs["routes"]
    object_to_count = combined_logs["logger_statuses"]
    
    report_formatter.group_by_count(group_by_object, object_to_count, report_name)
    
    
if __name__ == "__main__":
    start_time = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filenames", help="Файлы логов", nargs="+", type=str)
    parser.add_argument("-r", "--report", help="Название отчета", type=str, default="handler")
    args = parser.parse_args()
    filenames = args.filenames
    report_name = args.report
    main(filenames, report_name)
    execution_time = datetime.now() - start_time
    print("Программа завершена.\n"
          f"Время выполнения: {execution_time}")
    
