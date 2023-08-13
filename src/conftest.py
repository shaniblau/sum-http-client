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
def http_load_fixture():
    return HTTPLoad


@pytest.fixture
def app_fixture():
    return app


@pytest.fixture
def mock_requests(mocker):
    return mocker.patch.object(requests, 'post')


class MockObserver:
    def schedule(self, handler, path):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass


class MockFileClosedEvent:
    def __init__(self, src_path):
        self.src_path = src_path


class MockPool:
    def apply_async(self, func, args):
        pass


@pytest.fixture
def mock_observer(mocker):
    return mocker.patch('app.Observer', return_value=MockObserver())


@pytest.fixture
def mock_pool(mocker):
    return mocker.patch('app.pool', MockPool())


@pytest.fixture
def mock_event(mocker):
    return mocker.patch('app.FileClosedEvent', return_value=MockFileClosedEvent('/path/to/test_file.txt'))
