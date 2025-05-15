import pytest
from core import CSVParser
from app.columns import COLUMNS_AND_ALIASES, COLUMNS_ORIGINALS

def test_parse_columns():
    parser = CSVParser('tests/test_data/data1.csv')
    schema = parser._parse_columns()

    assert 'id' in schema
    assert 'name' in schema
    assert 'email' in schema
    assert 'rate' in schema['hourly_rate']

def test_missing_columns():
    with pytest.raises(ValueError) as exception:
        parser = CSVParser('tests/test_data/missing_field.csv')

    assert 'Missing fields: name' in str(exception.value)

def test_duplicated_columns():
    with pytest.raises(ValueError) as exception:
        parser = CSVParser('tests/test_data/duplicated_field.csv')

    assert 'name' in str(exception.value)
    assert 'hourly_rate,' in str(exception.value)
    assert 'salary' in str(exception.value)

def test_reports_added():
    parser = CSVParser('tests/test_data/data1.csv', 'tests/test_data/data2.csv', 'tests/test_data/data3.csv')

    assert ['3', 'carol@example.com', 'Carol Williams', 'Design', '170', '60'] in parser.reports
    assert ['201', 'karen@example.com', 'Karen White', 'Sales', '165', '50'] in parser.reports
    assert len(parser.reports) == parser.reports_size

def test_output():
    parser = CSVParser('tests/test_data/data1.csv', 'tests/test_data/data2.csv', 'tests/test_data/data3.csv')
    parser.output('name', 'email', 'department', calculated_fields_functions=['payout'])
    parser.output_group(group_by='hours_worked', calculated_group_fields_functions=['group_size'])
