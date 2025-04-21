from pathlib import Path
import ast

from log_parser.parser import DjangoRequestLogParser


correct_unit_test_log = """
                    2025-03-28 12:44:46,000 INFO django.request: 
                    GET /api/v1/reviews/ 404 OK [192.168.1.59]
                """
incorrect_unit_test_log = """
                    03-28-2025 44:46,000 LOG django.request: 
                    LOCK api/ 21 OK [1922.168.1.59]
                """
filepath = Path(__file__).parent.joinpath("test.log")
django_log_parser = DjangoRequestLogParser()
assert filepath.exists()

def test_correct_parsing():
    correct_logger_status = "INFO"
    correct_datetime = "2025-03-28 12:44:46"
    correct_method = "GET"
    correct_api = "/api/v1/reviews/"
    correct_response = "404"
    correct_source_ip = "192.168.1.59"
    extracted_logger_status = django_log_parser.extract_pattern(correct_unit_test_log,
                                                                django_log_parser.LOGGER_STATUSES)
    extracted_datetime = django_log_parser.extract_pattern(correct_unit_test_log,
                                                                django_log_parser.DATETIME)
    extracted_method = django_log_parser.extract_pattern(correct_unit_test_log,
                                                                django_log_parser.METHODS)
    extracted_api = django_log_parser.extract_pattern(correct_unit_test_log,
                                                                django_log_parser.ROUTES)
    extracted_source_ip = django_log_parser.extract_pattern(correct_unit_test_log,
                                                                django_log_parser.SOURCE)
    extracted_response = django_log_parser.extract_pattern(correct_unit_test_log,
                                                                django_log_parser.RESPONSE)
    assert extracted_logger_status == correct_logger_status
    assert extracted_datetime == correct_datetime
    assert extracted_method == correct_method
    assert extracted_api == correct_api
    assert extracted_source_ip == correct_source_ip
    assert extracted_response == correct_response
    
def test_incorrect_parsing():
    extracted_logger_status = django_log_parser.extract_pattern(incorrect_unit_test_log,
                                                                django_log_parser.LOGGER_STATUSES)
    extracted_datetime = django_log_parser.extract_pattern(incorrect_unit_test_log,
                                                                django_log_parser.DATETIME)
    extracted_method = django_log_parser.extract_pattern(incorrect_unit_test_log,
                                                                django_log_parser.METHODS)
    extracted_api = django_log_parser.extract_pattern(incorrect_unit_test_log,
                                                                django_log_parser.ROUTES)
    extracted_source_ip = django_log_parser.extract_pattern(incorrect_unit_test_log,
                                                                django_log_parser.SOURCE)
    extracted_response = django_log_parser.extract_pattern(incorrect_unit_test_log,
                                                                django_log_parser.RESPONSE)
    assert not ast.literal_eval(extracted_logger_status)
    assert not ast.literal_eval(extracted_method)
    assert not ast.literal_eval(extracted_api)
    assert not ast.literal_eval(extracted_source_ip)
    assert not ast.literal_eval(extracted_response)
    
def test_django_log_parser():
    log_examples = django_log_parser.get_file_lines(filepath)
    assert isinstance(log_examples, list)
    assert len(log_examples) == 101
    filtered_logs = django_log_parser.log_type_check(log_examples)
    assert isinstance(filtered_logs, list)
    assert len(filtered_logs) == 61
    structured_logs = django_log_parser.parse(filepath) 
    assert isinstance(structured_logs, dict)   
    assert "logger_statuses" in structured_logs
    assert "methods" in structured_logs
    assert "sources" in structured_logs
    assert "datetime" in structured_logs
    assert "routes" in structured_logs
    assert "responses" in structured_logs



