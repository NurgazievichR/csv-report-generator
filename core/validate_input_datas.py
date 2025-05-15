import os
from argparse import Namespace


def validate_input_data(args: Namespace) -> None:
    for filepath in args.files:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist")
        if not filepath.endswith(".csv"):
            raise ValueError(f"File {filepath} is not csv")

    from .decorators import reports_register

    reports_register_names: list[str] = [func.name for func in reports_register]
    if args.report not in reports_register_names:
        raise ValueError(f"There is no report {args.report}")
