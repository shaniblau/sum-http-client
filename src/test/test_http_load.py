import builtins
import os
from unittest.mock import patch
import requests

from help_funcs import create_files

files_names = ['file_a', 'file_b']


def test_create_files_should_be_list_of_upload_file_objects(http_load_fixture, mocker):
    mocker.patch('load.http_load.config.LOGS_DIR', './logs')
    mocker.patch('load.http_load.config.IMAGES_DIR_PATH', './')
    create_files()
    expected = []
    for name in files_names:
        with open(name, 'rb') as file:
            expected.append(("files", (name, file.read(), "image/jpg")))
    with patch('load.http_load.open',
               side_effect=lambda file, mode: builtins.open(os.path.abspath(file), mode)) as mock_file:
        result = http_load_fixture.create_files(files_names)
    assert expected.__str__() == result.__str__()


def test_load_file_should_be_200(http_load_fixture, mock_requests, mocker):
    mocker.patch('load.http_load.config.LOGS_DIR', './logs')
    mock_response = mock_requests()
    mock_response.status_code = 200
    response = http_load_fixture.load_files(files=[])
    assert response.status_code == 200


def test_log_response_should_log(http_load_fixture, mocker):
    mocker.patch('load.http_load.config.LOGS_DIR', './logs')
    mock_response = requests.Response()
    mock_response.status_code = 200
    http_load_fixture.log_response(mock_response, files_names)

