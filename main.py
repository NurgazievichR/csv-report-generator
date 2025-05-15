import argparse
from core import CSVParser, validate_input_data


def main():
    parser = argparse.ArgumentParser(
        description="Process CSV files and generate reports."
    )
    parser.add_argument("files", nargs="+", help="Paths to CSV files to process")
    parser.add_argument(
        "--report", type=str, required=True, help="Name of the report to generate"
    )
    args = parser.parse_args()
    validate_input_data(args)

    csv_parser = CSVParser(*args.files)
    csv_parser.call_report(args.report)


if __name__ == "__main__":
    main()
