import pytest

from db_integration import Redis, redis_client


@pytest.fixture
def redis_fixture():
    return Redis


@pytest.fixture
def redis_client_fixture():
    return redis_client
