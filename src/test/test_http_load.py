import requests
from help_funcs import create_files

files_names = ['file_a', 'file_b']


def test_execute_should_call_all_http_load_functions(http_load_fixture, mock_requests, mocker):
    create_files()
    files = []
    for name in files_names:
        with open(name, 'rb') as file:
            files.append(("files", (name, file.read(), "image/jpg")))
    mock_create_files = mocker.patch('load.http_load.HTTPLoad._HTTPLoad__create_files', return_value=files)
    mock_load_files = mocker.patch('load.http_load.HTTPLoad._HTTPLoad__load_files', return_value=requests.Response)
    mock_log_response = mocker.patch('load.http_load.HTTPLoad._HTTPLoad__log_response')
    mock_delete_files = mocker.patch('load.http_load.HTTPLoad._HTTPLoad__delete_files')
    http_load_fixture.execute(files_names)
    mock_create_files.assert_called_once_with(files_names)
    mock_load_files.assert_called_once_with(files, files_names)
    mock_log_response.assert_called_once_with(requests.Response, files_names)
    mock_delete_files.assert_called_once_with(files_names)

