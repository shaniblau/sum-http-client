from queue import Queue
from unittest.mock import MagicMock

from app import Handler
from help_funcs import create_queue


def test_run_should_call_handle_existing_files_and_observer(app_fixture, mocker):
    mock_handle_files = mocker.patch('app.handle_existing_files')
    mock_observer = mocker.patch('app.Observer')
    mocker.patch('app.time.sleep', side_effect=KeyboardInterrupt)
    app_fixture.run()
    mock_handle_files.assert_called_once()
    mock_observer.assert_called()


# def test_handle_existing_files_should_create_a_process_for_each_file(app_fixture, mocker, mock_pool):
#     mocker.patch('app.os.listdir', return_value=['file1.txt', 'file2.txt'])
#     mocker.patch('app.pool', mock_pool)
#     app_fixture.handle_existing_files()
#     mock_pool.apply_async.assert_called()
#     assert mock_pool.apply_async.call_count == 2


def test_process_event(app_fixture, mocker):
    mock_event = mocker.Mock()
    mocker.patch('your_module.Redis.check_existence', return_value=True)
    mocker.patch('your_module.Redis.extract', return_value='first_half')
    mocker.patch('your_module.HTTPLoad.execute')
    mocker.patch('your_module.Redis.load')
    app_fixture.process_event(mock_event)
    assert app_fixture.Redis.check_existence.called
    assert app_fixture.Redis.extract.called
    app_fixture.HTTPLoad.execute.assert_called()
    app_fixture.Redis.load.assert_called()

