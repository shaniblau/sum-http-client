import pytest
import requests

import app
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
    mocker.patch('load.http_load.config.LOGS_DIR', './logs')
    return HTTPLoad


@pytest.fixture
def app_fixture(mocker):
    mocker.patch('app.config.LOGS_DIR', './')
    return app


@pytest.fixture
def mock_requests(mocker):
    return mocker.patch.object(requests, 'post')
