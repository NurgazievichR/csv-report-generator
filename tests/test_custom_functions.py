import pytest

from core import (
    CSVParser,
    calculate_field_functions_register,
    calculate_group_field_functions_register,
    reports_register,
)


@pytest.fixture(scope="module")
def parser():
    return CSVParser(
        "tests/test_data/data1.csv",
        "tests/test_data/data2.csv",
        "tests/test_data/data3.csv",
    )


def test_calculate_field_functions(parser):
    report = parser.reports[0]
    data_dict = {
        key: int(val) if val.isdigit() else val
        for key, val in zip(parser.headers, report)
    }

    for func in calculate_field_functions_register:
        func(data_dict)


def test_calculate_group_field_functions(parser):
    data_dict = parser.generate_groups()

    for func in calculate_group_field_functions_register:
        for group_key, group_values in data_dict.items():
            group_values["group_size"] = len(group_values["id"])
            func(group_values)


def test_report_functions(parser):
    for func in reports_register:
        func(parser)
