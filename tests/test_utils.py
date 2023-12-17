import pytest
from unittest.mock import patch
from src.utils import read_csv_from_path, save_output
from contextlib import ExitStack as DoesNotRaise


def test_valid_csv_file():
    with patch(
            "src.utils.os.path.isfile",
            return_value=True
    ) as os_isfile_mock, patch(
        "src.utils.pd.read_csv",
        return_value='mock result'
    ) as pd_read_mock:
        test_file_path = 'notaCSVfile'
        with pytest.raises(Exception) as exc_info:
            observed = read_csv_from_path(test_file_path)
            os_isfile_mock.assert_called_once()
            pd_read_mock.assert_not_called()
            assert observed is None
            assert exc_info is ValueError("Invalid file format. Please provide a CSV file.")

        test_file_path = 'valid.csv'
        with pytest.raises(Exception) as exc_info:
            observed = read_csv_from_path(test_file_path)
            os_isfile_mock.assert_called_once()
            pd_read_mock.assert_called_once_with(test_file_path)
            assert observed == 'mock result'
            assert type(exc_info.value.__cause__) is DoesNotRaise()

    with patch(
            "src.utils.os.path.isfile",
            return_value=False
    ) as not_file_mock, patch(
        "src.utils.pd.read_csv"
    ) as read_not_called:
        test_file_path = 'not a file'
        with pytest.raises(Exception) as exc_info:
            observed = read_csv_from_path(test_file_path)
            not_file_mock.assert_called_once()
            read_not_called.assert_not_called()
            assert observed is None
            assert exc_info is ValueError("Please enter a valid file path and make sure the file exists")


def test_save_output():
    with patch(
            "src.utils.open"
    ) as mock_open, patch(
        "src.utils.json.dump"
    ) as mock_json_dump:
        output = {'key': 'value'}
        path = 'path/to/mock_output.json'
        save_output(output, path)
        mock_open.assert_called_once_with(path, 'w')
        mock_json_dump.assert_called_once_with(output, mock_open().__enter__())
