from core import CSVParser
from core import report_decorator

@report_decorator()
def payout(obj: CSVParser):
    obj.output(calculated_fields_functions=['payout'])

@report_decorator()
def average_hourly_rate_in_department(obj: CSVParser):
    obj.output_group(group_by='department', calculated_group_fields_functions=['average_hourly_rate'])

