from app.columns import COLUMNS_AND_ALIASES, COLUMNS_ORIGINALS
from .decorators import calculate_field_functions_register, calculate_group_field_functions_register, reports_register

COLUMNS_COUNT = len(COLUMNS_AND_ALIASES)
COLUMN_INDEXES = {COLUMNS_ORIGINALS[i]: i for i in range(COLUMNS_COUNT)}

class CSVParser:
    def __init__(self, *filepaths:str):
        self.files = filepaths
        self.reports = []
        self.reports_size = 0
        self.schema = self._parse_columns()
        self.columns_longest_sizes = [len(COLUMNS_ORIGINALS[i]) for i in range(COLUMNS_COUNT)]
        self.headers = [COLUMNS_ORIGINALS[i] for i in range(COLUMNS_COUNT)]
        self.shift = 3

        for file in self.files:
            self._process_file(file)
        self.reports_size = len(self.reports)
        self.reports.sort(key=lambda x: (x[3]))

        self.calc_field_funtions = calculate_field_functions_register
        self.calc_group_filed_frunctions = calculate_group_field_functions_register
        self.report_functions = reports_register

    def _parse_columns(self):
        schema = {}
        for i in range(COLUMNS_COUNT):
            original = COLUMNS_ORIGINALS[i]
            aliases = set(COLUMNS_AND_ALIASES[i])
            schema[original] = aliases
        return schema

    def _map_headers(self, header_row):
        column_occurrences = [0 for i in range(COLUMNS_COUNT)]
        mapped_headers = ["" for i in range(len(header_row))]

        for i in range(len(header_row)):
            header = header_row[i]
            for original, aliases in self.schema.items():
                if header in aliases:
                    column_occurrences[COLUMN_INDEXES[original]] += 1
                    mapped_headers[i] = original

        # На всякий, если неправильно переданы данные
        missing_fields = [COLUMNS_ORIGINALS[i] for i in range(COLUMNS_COUNT) if not column_occurrences[i]]
        if missing_fields:
            raise ValueError(f"Missing fields: {", ".join(missing_fields)}")

        duplicate_fields = [tuple(column for column in COLUMNS_AND_ALIASES[i] if column in header_row) for i in range(COLUMNS_COUNT) if column_occurrences[i] > 1]
        if duplicate_fields:
            formatted_fields = [f"({', '.join(field)})" for field in duplicate_fields]
            raise ValueError(f"Duplicated fields: {', '.join(formatted_fields)}")

        return mapped_headers

    def _process_file(self, file):
        with open(file, 'r') as f:
            header_row = f.readline().strip().split(',')
            headers = self._map_headers(header_row)

            for line in f:
                values = line.strip().split(',')
                ordered_values = ["" for i in range(len(values))]
                for i in range(len(values)):
                    ordered_values[COLUMN_INDEXES[headers[i]]] = values[i]
                    self.columns_longest_sizes[COLUMN_INDEXES[headers[i]]] = max(self.columns_longest_sizes[COLUMN_INDEXES[headers[i]]], len(values[i]))
                self.reports.append(ordered_values)

    #Printing
    def _print_headers(self, fields_to_print, calculated_fields_functions):
        print("".ljust(self.columns_longest_sizes[COLUMN_INDEXES['department']] + self.shift), end='')
        for i in range(len(self.headers)):
            if fields_to_print[i]:
                print(self.headers[i].ljust(self.columns_longest_sizes[i] + self.shift), end='')
        for func in self.calc_field_funtions:
            if func.name in calculated_fields_functions:
                print(func.name.ljust(func.max_size + self.shift), end='')
        print()

    def _print_row(self, report, fields_to_print):
        print("".ljust(self.columns_longest_sizes[COLUMN_INDEXES['department']] + self.shift - 1, '-'), end=' ')
        for i in range(len(report)):
            if fields_to_print[i]:
                print(str(report[i]).ljust(self.columns_longest_sizes[i] + self.shift), end='')

    def _print_calculated_data(self, report, calculated_fields_functions):
        report_dct = {}
        for i in range(len(report)):
            report_dct[COLUMNS_ORIGINALS[i]] = int(report[i]) if report[i].isdigit() else report[i]
        for func in self.calc_field_funtions:
            if func.name in calculated_fields_functions:
                print(str(func(report_dct)).ljust(func.max_size + self.shift), end='')
        print()

    def output(self, *args, calculated_fields_functions=None):
        if args:
            fields_to_print = [COLUMNS_ORIGINALS[i] in args and COLUMNS_ORIGINALS[i] != 'department' for i in
                               range(COLUMNS_COUNT)]
        else:
            fields_to_print = [COLUMNS_ORIGINALS[i] != 'department' for i in range(COLUMNS_COUNT)]
        i = 0
        curr_group = self.reports[i][COLUMN_INDEXES['department']]
        self._print_headers(fields_to_print, calculated_fields_functions)
        print(curr_group)
        while i < self.reports_size:
            if curr_group != self.reports[i][COLUMN_INDEXES['department']]:
                curr_group = self.reports[i][COLUMN_INDEXES['department']]
                print(curr_group)

            self._print_row(self.reports[i], fields_to_print)
            self._print_calculated_data(self.reports[i], calculated_fields_functions)
            i += 1

    def output_group(self, group_by='department', calculated_group_fields_functions = None):
        print(group_by.ljust(self.columns_longest_sizes[COLUMN_INDEXES[group_by]] + self.shift), end='')

        for func in self.calc_group_filed_frunctions:
            if func.name in calculated_group_fields_functions:
                print(func.name.ljust(func.max_size + self.shift), end='')
        print()

        groups = {}
        for report in self.reports:
            group = report[COLUMN_INDEXES[group_by]]
            if groups.get(group) is None:
                groups[group] = {}
            for i in range(len(report)):
                if groups[group].get(COLUMNS_ORIGINALS[i]) is None:
                    groups[group][COLUMNS_ORIGINALS[i]] = []
                groups[group][COLUMNS_ORIGINALS[i]].append(int(report[i]) if report[i].isdigit() else report[i])

        for group_key, group_data in groups.items():
            group_data['group_size'] = len(group_data['id'])
            print(group_key.ljust(self.columns_longest_sizes[COLUMN_INDEXES[group_by]] + self.shift), end='')

            for func in self.calc_group_filed_frunctions:
                if func.name in calculated_group_fields_functions:
                    print(str(func(group_data)).ljust(func.max_size + self.shift), end='')
            print()

    def call_report(self, report:str):
        for func in self.report_functions:
            if func.name == report:
                func(self)