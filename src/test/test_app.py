import logging


def test_process_file_invalid_file_name_should_log_error(app_fixture, caplog):
    expected = 'the file file_c.txt name is not in the requested format'
    app_fixture.process_file('/file_c.txt')
    error_messages = [record[2] for record in caplog.record_tuples if record[1] == logging.ERROR]
    assert expected == error_messages[0]
    assert len(error_messages) == 1


def test_process_file_invalid_parameter_should_log_error(app_fixture, caplog):
    expected = "the files were not sent do to: 'int' object has no attribute 'split'"
    app_fixture.process_file(5)
    error_messages = [record[2] for record in caplog.record_tuples if record[1] == logging.ERROR]
    assert expected == error_messages[0]
    assert len(error_messages) == 1


def test_process_file_should_call_handle_half(app_fixture, mocker):
    mock_handle_half = mocker.patch('app.handle_half')
    app_fixture.process_file('/files/file_a.txt')
    mock_handle_half.assert_called_once()


def test_handle_half_first_half_should_call_redis_load_and_not_call_handle_second_half(app_fixture, mocker):
    mock_load = mocker.patch('app.Redis.load', return_value=1)
    mock_handle_second_half = mocker.patch('app.handle_second_half')
    app_fixture.handle_half('file_a.txt', 'file')
    mock_load.assert_called_once_with('file_a.txt', 'file')
    mock_handle_second_half.assert_not_called()


def test_handle_half_second_half_should_call_loaded_and_handle_second_half(app_fixture, mocker):
    mock_load = mocker.patch('app.Redis.load', return_value=0)
    mock_handle_second_half = mocker.patch('app.handle_second_half')
    app_fixture.handle_half('file_a.txt', 'file')
    mock_load.assert_called_once_with('file_a.txt', 'file')
    mock_handle_second_half.assert_called_once_with('file', 'file_a.txt')


def test_handle_second_half_2_identical_files_names_should_log_error_and_call_redis_load(app_fixture, mocker, caplog):
    mocker.patch('app.Redis.extract', return_value='file_a.txt')
    mock_load = mocker.patch('app.Redis.load')
    mock_execute = mocker.patch('app.HTTPLoad.execute')
    app_fixture.handle_second_half('file', 'file_a.txt')
    expected = "the file file_a.txt has been sent twice"
    error_messages = [record[2] for record in caplog.record_tuples if record[1] == logging.WARNING]
    assert expected == error_messages[0]
    assert len(error_messages) == 1
    mock_load.assert_called_once_with('file_a.txt', 'file')
    mock_execute.assert_not_called()


def test_handle_second_half_should_call_http_load_execute(app_fixture, mocker, caplog):
    mocker.patch('app.Redis.extract', return_value='file_a.txt')
    mock_execute = mocker.patch('app.HTTPLoad.execute')
    mock_load = mocker.patch('app.Redis.load')
    app_fixture.handle_second_half('file', 'file_b')
    mock_execute.assert_called_once_with(['file_a.txt', 'file_b'])
    mock_load.assert_not_called()
