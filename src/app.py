import logging as log
import os
import time
from datetime import datetime
from multiprocessing.pool import Pool

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileClosedEvent

from configuration import config
from load import HTTPLoad, error_logger
from db_integration import Redis
from set_logger import extendable_logger

date = datetime.now().strftime("%d_%m_%Y")
arrived_logger = extendable_logger(f'{config.LOGS_DIR}/files-arrived/{date}.log', log.INFO)
pool = Pool()


def run():
    observer = Observer()
    handle_existing_files()
    event_handler = Handler()
    observer.schedule(event_handler, config.IMAGES_DIR_PATH)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        pool.close()
    pool.join()
    observer.join()


def handle_existing_files():
    for file in os.listdir(config.IMAGES_DIR_PATH):
        file_path = os.path.join(config.IMAGES_DIR_PATH, file)
        event = FileClosedEvent(file_path)
        pool.apply_async(func=process_event, args=(event,))


def process_event(event):
    try:
        arrived_logger.info(f'the file {event.src_path} has been received')
        file_name: str = event.src_path.split("/")[-1]
        file_full_name = file_name.split("_")[0].split('.')[0]
        if "_a" == file_name[-2:] and "_b" == file_name[-2:]:
            error_logger.error(f'the file {file_name} name is not in the requested format')
        else:
            handle_file(file_name, file_full_name)
    except Exception as e:
        error_logger.error(f'the files were not sent do to: {e}')


def handle_file(file_name, file_full_name):
    if Redis.check_existence(file_full_name):
        first_half = Redis.extract(file_full_name)
        second_half = file_name
        if second_half != first_half:
            HTTPLoad.execute([first_half, second_half])
        else:
            error_logger.warning(f'the file {file_name} has been sent twice')
            Redis.load(file_name, file_full_name)
    else:
        Redis.load(file_name, file_full_name)


class Handler(FileSystemEventHandler):
    def on_closed(self, event):
        pool.apply_async(func=process_event, args=(event,))
