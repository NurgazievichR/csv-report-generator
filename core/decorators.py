from functools import wraps
from typing import Callable, Any, Union

calculate_field_functions_register: list[Callable[[dict], Union[str, int]]] = []
calculate_group_field_functions_register: list[Callable[[dict], Union[str, int]]] = []
reports_register: list[Callable[["CSVParser"], None]] = []


def calculated_field_decorator(max_size=10, name=None, group=False) -> Callable:
    def decorator(func):
        @wraps(func)
        def wrapper(dct):
            return func(dct)

        wrapper.name = name if name else func.__name__
        wrapper.max_size = max(max_size, len(wrapper.name))

        if group:
            calculate_group_field_functions_register.append(wrapper)
        else:
            calculate_field_functions_register.append(wrapper)

        return wrapper

    return decorator


def report_decorator(name=None) -> Callable:
    def decorator(func):
        @wraps(func)
        def wrapper(dct):
            return func(dct)

        wrapper.name = name if name else func.__name__
        reports_register.append(wrapper)

        return wrapper

    return decorator
