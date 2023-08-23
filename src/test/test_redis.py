from help_funcs import redis_cleanup


def test_check_existence_should_be_false(redis_fixture):
    expected = False
    result = redis_fixture.check_existence('file.jpg')
    assert expected == result


def test_load_should_be_true(redis_fixture, redis_client_fixture):
    redis_fixture.load('file_a', 'file.jpg')
    expected = True
    result = redis_fixture.check_existence('file.jpg')
    redis_cleanup(redis_client_fixture, 'file.jpg')
    assert expected == result


# def test_extract_should_be_file_a(redis_fixture, redis_client_fixture):
#     redis_fixture.load('file_a', 'file.jpg')
#     result = redis_fixture.extract('file.jpg')
#     expected = 'file_a'
#     redis_cleanup(redis_client_fixture, 'file.jpg')
#     assert result == expected
