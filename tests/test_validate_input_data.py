from unittest.mock import patch

import pytest

from core import validate_input_data


class Args:
    def __init__(self, files, report="payout"):
        self.files = files
        self.report = report


def test_file_not_found():
    args = Args(files=["nonexistent_file1", "nonexistent_file2"])
    with pytest.raises(FileNotFoundError) as exception:
        validate_input_data(args)
    assert ("nonexistent_file1") in str(exception.value)


@patch("core.validate_input_datas.os.path.isfile", return_value=True)
def test_file_wrong_extension(mock_isfile):
    args = Args(files=["file1.txt", "file2.csv", "file3.exe"])
    with pytest.raises(ValueError) as exception:
        validate_input_data(args)
    assert ("is not csv") in str(exception.value)


def test_wrong_report():
    args = Args(
        files=[
            "tests/test_data/data1.csv",
            "tests/test_data/data2.csv",
            "tests/test_data/data3.csv",
        ],
        report="nonexistent_report",
    )
    with pytest.raises(ValueError) as exception:
        validate_input_data(args)


def test_all_files_valid_real():
    args = Args(
        files=[
            "tests/test_data/data1.csv",
            "tests/test_data/data2.csv",
            "tests/test_data/data3.csv",
        ],
    )
    validate_input_data(args)
