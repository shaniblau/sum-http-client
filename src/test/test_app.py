from queue import Queue
from unittest.mock import MagicMock
from help_funcs import create_queue


def test_run(app_fixture, mocker, mock_observer, mock_pool):
    mock_handle_files = mocker.patch('app.handle_existing_files')
    mocker.patch('app.time.sleep', side_effect=KeyboardInterrupt)
    app_fixture.run()
    mock_handle_files.assert_called_once()
    mock_observer.assert_called()
    mock_observer.return_value.schedule.assert_called()
    mock_observer.return_value.start.assert_called()
