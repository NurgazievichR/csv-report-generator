from functools import wraps

calculate_field_functions_register = []
calculate_group_field_functions_register = []
reports_register = []

def calculated_field_decorator(max_size=10, name=None, group=False):
    def decorator(func):

        @wraps(func)
        def wrapper(dct):
            return func(dct)

        new_name = name if name else func.__name__
        wrapper.max_size = max(max_size, len(new_name))
        wrapper.name = new_name

        if group:
            calculate_group_field_functions_register.append(wrapper)
        else:
            calculate_field_functions_register.append(wrapper)

        return wrapper
    return decorator

def report_decorator(name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(dct):
            return func(dct)

        wrapper.name = name if name else func.__name__
        reports_register.append(wrapper)

        return wrapper
    return decorator

