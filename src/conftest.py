import pytest
import requests

from db_integration import Redis, redis_client
from load import HTTPLoad


@pytest.fixture
def redis_fixture():
    return Redis


@pytest.fixture
def redis_client_fixture():
    return redis_client


@pytest.fixture
def http_load_fixture():
    return HTTPLoad


@pytest.fixture
def mock_requests(mocker):
    return mocker.patch.object(requests, 'post')
