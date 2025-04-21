from pathlib import Path
from itertools import combinations_with_replacement

from report_formatter.report_formatter import ReportFormatter
from log_parser.parser import DjangoRequestLogParser
from utils import combine_dicts


filepath = Path(__file__).parent.joinpath("test.log")
django_log_parser = DjangoRequestLogParser()
report_formatter = ReportFormatter()
assert filepath.exists()

def test_formatter():
    structured_logs = django_log_parser.parse(filepath)
    logs_keys = structured_logs.keys()
    
    key_pairs = combinations_with_replacement(logs_keys, 2)
    _ = [
        report_formatter.group_by_count(structured_logs[a], structured_logs[b], "TEST_DECART")
        for a, b in key_pairs
    ]