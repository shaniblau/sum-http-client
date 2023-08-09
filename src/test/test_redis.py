from help_funcs import redis_cleanup


def test_check_existence(redis_fixture):
    expected = False
    result = redis_fixture.check_existence('file.jpg')
    assert expected == result


def test_load(redis_fixture):
    redis_fixture.load('file_a', 'file.jpg')
    expected = True
    result = redis_fixture.check_existence('file.jpg')
    redis_cleanup('file.jpg')
    assert expected == result


def test_extract(redis_fixture):
    redis_fixture.load('file_a', 'file.jpg')
    result = redis_fixture.extract('file.jpg')
    expected = 'file_a'
    redis_cleanup('file.jpg')
    assert result == expected
