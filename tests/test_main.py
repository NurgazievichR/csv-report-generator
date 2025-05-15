import pytest
import sys
import main

list_of_test = [
    (('tests/test_data/data1.csv', 'tests/test_data/data2.csv', 'tests/test_data/data3.csv'), 'payout', None),
    (('tests/test_data/data1.csv', 'tests/test_data/data2.csv', 'tests/test_data/data3.csv'), '', SystemExit),
    ((), 'payout', SystemExit),
    (('tests/test_data/data1.csv', 'nonexist.csv', 'tests/test_data/data3.csv'), 'payout', FileNotFoundError),
    (('tests/test_data/data1.csv', 'tests/test_data/data2.csv', 'tests/test_data/data3.csv'), 'nonexist', ValueError),
]

@pytest.mark.parametrize("files, report, expected_error", list_of_test)
def test_main_parametrized(monkeypatch, files, report, expected_error):
    argv = ['prog']
    argv.extend(files)
    if report:
        argv.extend(['--report', report])

    monkeypatch.setattr(sys, 'argv', argv)

    if expected_error is None:
        main.main()
    else:
        with pytest.raises(expected_error):
            main.main()