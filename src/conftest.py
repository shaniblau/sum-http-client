import pytest

from db_integration import Redis


@pytest.fixture
def redis_fixture():
    return Redis
