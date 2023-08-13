import builtins
import os
from unittest.mock import patch

import requests

from help_funcs import create_files

files_names = ['file_a', 'file_b']


def test_create_files(http_load_fixture, mocker):
    mocker.patch('load.http_load.config.LOGS_DIR', './logs')
    create_files()
    expected = [('files', ('file_a', open('./file_a', "rb"), "image/jpg")),
                ('files', ('file_b', open('./file_b', "rb"), "image/jpg"))]
    with patch('load.http_load.HTTPLoad.open',
               side_effect=lambda file, mode: builtins.open(os.path.abspath(file), mode)) as mock_file:
        result = http_load_fixture.create_files(files_names)
    assert expected.__str__() == result.__str__()
#
#
# def test_upload_file(http_load_fixture, mock_requests):
#     mock_response = mock_requests()
#     mock_response.status_code = 200
#     response = http_load_fixture.upload_files(files=[])
#     assert response.status_code == 200
#
#
# def test_log_response(http_load_fixture):
#     mock_response = requests.Response()
#     mock_response.status_code = 200
#     http_load_fixture.log_response(mock_response, files_names)
#
#
# def test_delete_files(http_load_fixture, mocker):
#     mocker.patch('os.remove')
#     http_load_fixture.delete_files(files_names)
#
