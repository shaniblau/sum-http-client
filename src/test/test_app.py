def test_process_file_invalid_file_name_should_log_error(app_fixture, caplog):
    app_fixture.process_file('/file_c.txt')
    assert caplog.record_tuples == ['the file file_c name is not in the requested format']


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
