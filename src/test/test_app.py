from queue import Queue
from unittest.mock import MagicMock
from help_funcs import create_queue


def test_process_queue(app_fixture):
    q = create_queue()
    returned = app_fixture.process_queue(q)
    expected = 'the file file1_c name is not in the requested format'
    assert returned == expected


def test_handler(app_fixture):
    q = Queue()
    handler = app_fixture.Handler(q)
    event = MagicMock()
    handler.on_closed(event)
    assert q.get() == event
