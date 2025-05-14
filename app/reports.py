from core import CSVParser
from core import report_decorator

@report_decorator()
def payout(obj: CSVParser):
    obj.output('name', 'hours', 'hourly_rate', calculated_fields_functions=['payout'])

@report_decorator()
def s(obj: CSVParser):
    obj.output(calculated_fields_functions=['payout'])

