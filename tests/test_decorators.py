import inspect

import pytest

import app.calculated_fields as calc
import app.calculated_group_fields as calc_group
import app.reports as reports_
from core import (
    CSVParser,
    calculate_field_functions_register,
    calculate_group_field_functions_register,
    calculated_field_decorator,
    report_decorator,
    reports_register,
)


def test_all_functions_reports_registered():
    field_functions = {
        name for name, func in inspect.getmembers(calc, inspect.isfunction)
    }
    field_group_functions = {
        name for name, func in inspect.getmembers(calc_group, inspect.isfunction)
    }
    reports = {name for name, func in inspect.getmembers(reports_, inspect.isfunction)}

    registered_field_functions = {
        func.__name__ for func in calculate_field_functions_register
    }
    registered_group_functions = {
        func.__name__ for func in calculate_group_field_functions_register
    }
    registered_reports = {func.__name__ for func in reports_register}

    assert registered_field_functions.issubset(
        field_functions
    ), "Не все field functions зарегистрированы"
    assert registered_group_functions.issubset(
        field_group_functions
    ), "Не все group field functions зарегистрированы"
    assert registered_reports.issubset(
        reports
    ), "Не все report functions зарегистрированы"


def test_decorators_register_functions():
    @calculated_field_decorator(max_size=15, name="custom_func")
    def custom_func(dct):
        return dct["hours_worked"] * 2

    @calculated_field_decorator(max_size=5, name="custom_group_func", group=True)
    def custom_group_func(dct):
        return sum(dct["hours_worked"])

    @report_decorator(name="custom_report")
    def custom_report(obj: CSVParser):
        obj.output()

    assert (
        custom_func in calculate_field_functions_register
    ), "custom_func не зарегистрирована в calculate_field_functions_register"
    assert (
        custom_group_func in calculate_group_field_functions_register
    ), "custom_group_func не зарегистрирована в calculate_group_field_functions_register"
    assert (
        custom_report in reports_register
    ), "custom_report не зарегистрирован в reports_register"

    assert custom_func.name == "custom_func", "custom_func.name не совпадает"
    assert custom_func.max_size == 15, "custom_func.max_size неверен"

    assert (
        custom_group_func.name == "custom_group_func"
    ), "custom_group_func.name не совпадает"
    assert custom_group_func.max_size == 17, "custom_group_func.max_size неверен"

    assert custom_report.name == "custom_report", "custom_report.name не совпадает"

    assert (
        custom_group_func not in calculate_field_functions_register
    ), "custom_group_func не должна быть в calculate_field_functions_register"
