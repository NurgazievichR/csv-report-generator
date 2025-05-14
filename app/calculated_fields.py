from core import calculated_field_decorator

#Write dct keys according to settings.COLUMNS_ORIGINALS

@calculated_field_decorator(max_size=10)
def payout(dct: dict):
    return dct['hourly_rate'] * dct['hours_worked']

@calculated_field_decorator(max_size=10)
def payout_year(dct: dict):
    return dct['hourly_rate'] * dct['hours_worked'] * 12

@calculated_field_decorator(max_size=10)
def first_name(dct: dict):
    return dct['name'].split()[0]

