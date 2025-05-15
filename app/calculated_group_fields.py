from core import calculated_field_decorator

#Write dct keys according to settings.COLUMNS_ORIGINALS

@calculated_field_decorator(max_size=10, group=True)
def average_hourly_rate(dct: dict):
    group_size = dct['group_size']
    result = 0
    for i in range(group_size):
        result += dct['hourly_rate'][i]
    result /= group_size
    return f"{result:.2f}"

@calculated_field_decorator(max_size=10, group=True)
def group_size(dct: dict):
    return dct['group_size']

