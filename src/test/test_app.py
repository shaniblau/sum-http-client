import logging


def test_process_file_invalid_file_name_should_log_error(app_fixture, caplog):
    expected = 'the file file_c name is not in the requested format'
    app_fixture.process_file('/file_c.txt')
    error_messages = [record for record in caplog.record_tuples if record[1] == logging.ERROR]
    error_message_texts = [record[2] for record in error_messages]
    assert expected in error_message_texts


def test_process_file_invalid_parameter_should_log_error(app_fixture):
    pass


def test_process_file_should_call_handle_half(app_fixture):
    pass


def test_handle_half_identical_files_names(app_fixture):
    pass


def test_handle_half_new_file_should_call_redis_load(app_fixture):
    pass


def test_handle_half_existing_file_should_call_http_load_execute(app_fixture):
    pass
