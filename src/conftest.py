import pytest

from db_integration import Redis, redis_client
from load import HTTPLoad


@pytest.fixture
def redis_fixture():
    return Redis


@pytest.fixture
def redis_client_fixture():
    return redis_client


@pytest.fixture
def http_load_fixture(mocker):
    mocker.patch('load.http_load.sent_logger')
    return HTTPLoad
