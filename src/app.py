import logging as log
from multiprocessing import Queue
import os
import time
from datetime import datetime
from multiprocessing import Process


from multiprocessing.pool import Pool
from threading import Thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileClosedEvent

from configuration import config
from load import HTTPLoad, error_logger
from db_integration import Redis
from set_logger import extendable_logger

date = datetime.now().strftime("%d_%m_%Y")
arrived_logger = extendable_logger(f'{config.LOGS_DIR}/files-arrived/{date}.log', log.INFO)


def run():
    observer = Observer()
    watchdog_queue = Queue()
    handle_existing_files(watchdog_queue)
    worker = Process(target=process_queue, args=(watchdog_queue,), daemon=True)
    worker.start()
    event_handler = Handler(watchdog_queue)
    observer.schedule(event_handler, config.IMAGES_DIR_PATH)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        worker.close()
    observer.join()
    worker.join()


def handle_existing_files(watchdog_queue):
    for file in os.listdir(config.IMAGES_DIR_PATH):
        file_path = os.path.join(config.IMAGES_DIR_PATH, file)
        event = FileClosedEvent(file_path)
        watchdog_queue.put(event)


def process_queue(q):
    while True:
        if not q.empty():
            event = q.get()
            arrived_logger.info(f'the file {event.src_path} has been received')
            file_name: str = event.src_path.split("/")[-1]
            file_full_name = file_name.split("_")[0].split('.')[0]
            if "_a" == file_name[-2:] and "_b" == file_name[-2:]:
                error_logger.error(f'the file {file_name} name is not in the requested format')
            else:
                handle_file(file_name, file_full_name)


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


def start_multi_processing(q):
    while True:
        try:
            process_queue(q)
        except Exception:
            error_logger.error(f'the files were not sent do to: {Exception.__str__}')


class Handler(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_closed(self, event):
        self.queue.put(event)
