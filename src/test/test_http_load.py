import builtins
import os
from unittest.mock import patch
import requests
from help_funcs import create_files

files_names = ['file_a', 'file_b']


def test_execute(http_load_fixture, mock_requests, mocker):
    create_files()
    files = []
    for name in files_names:
        with open(name, 'rb') as file:
            files.append(("files", (name, file.read(), "image/jpg")))
    mock_create_files = mocker.patch('load.http_load.HTTPLoad.create_files', return_value=files)
    mock_load_files = mocker.patch('load.http_load.HTTPLoad.load_files', return_value=requests.Response)
    mock_log_response = mocker.patch('load.http_load.HTTPLoad.log_response')
    mock_delete_files = mocker.patch('load.http_load.HTTPLoad.delete_files')
    http_load_fixture.execute(files_names)
    mock_create_files.assert_called_once_with(files_names)
    mock_load_files.assert_called_once_with(files)
    mock_log_response.assert_called_once_with(requests.Response, files_names)
    mock_delete_files.assert_called_once_with(files_names)


def test_create_files_should_be_list_of_upload_file_objects(http_load_fixture, mocker):
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


def test_load_file_should_be_200(http_load_fixture, mock_requests):
    mock_response = mock_requests()
    mock_response.status_code = 200
    response = http_load_fixture.load_files(files=[])
    assert response.status_code == 200
