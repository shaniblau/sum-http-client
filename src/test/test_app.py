from queue import Queue
from unittest.mock import MagicMock

from app import Handler
from help_funcs import create_queue


def test_run_should_call_other_funcs(app_fixture, mocker):
    mock_handle_files = mocker.patch('app.handle_existing_files')
    mock_observer = mocker.patch('app.observer')
    mocker.patch('app.time.sleep', side_effect=KeyboardInterrupt)
    app_fixture.run()
    mock_handle_files.assert_called_once()
    mock_observer.schedule.assert_called_with(app_fixture.Handler(), app_fixture.config.IMAGES_DIR_PATH)


def test_handle_existing_files_should_create_a_process_for_each_file(app_fixture):
    pass
