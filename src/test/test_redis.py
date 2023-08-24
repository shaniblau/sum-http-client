from help_funcs import redis_cleanup


def test_load_first_half_should_return_1_and_call_expire(redis_fixture, redis_client_fixture, mocker):
    mock_expire = mocker.patch('db_integration.Redis.redis_client.expire')
    expected = 1
    result = redis_fixture.load('file_a', 'file')
    redis_cleanup(redis_client_fixture, 'file.jpg')
    mock_expire.assert_called_once_with('file', 60)
    assert expected == result


def test_load_second_half_should_return_0_and_not_call_expire(redis_fixture, redis_client_fixture, mocker):
    mock_expire = mocker.patch('db_integration.Redis.redis_client.expire')
    expected = 0
    redis_fixture.load('file_b.jpg', 'file')
    result = redis_fixture.load('file_a', 'file')
    redis_cleanup(redis_client_fixture, 'file.jpg')
    mock_expire.assert_not_called()
    assert expected == result


def test_extract_should_be_file_a(redis_fixture, redis_client_fixture):
    redis_fixture.load('file_a', 'file.jpg')
    result = redis_fixture.extract('file.jpg')
    expected = 'file_a'
    redis_cleanup(redis_client_fixture, 'file.jpg')
    assert result == expected
