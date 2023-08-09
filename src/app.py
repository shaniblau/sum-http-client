import logging as log
import os
import time
from datetime import datetime
from queue import Queue

from multiprocessing import Process
from multiprocessing.pool import Pool
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileClosedEvent

from configuration import config
from load import HTTPLoad, error_logger
from db_integration import Redis
from set_logger import extendable_logger

date = datetime.now().strftime("%d_%m_%Y")
arrived_logger = extendable_logger(f'./logs/files-arrived/{date}.log', log.INFO)


def run():
    observer = Observer()
    watchdog_queue = Queue()
    handle_existing_files(watchdog_queue)
    with Pool() as pool:
        pass
    worker = Process(target=start_multi_processing(watchdog_queue), args=(watchdog_queue,), daemon=True)
    worker.start()
    event_handler = Handler(watchdog_queue)
    observer.schedule(event_handler, config.IMAGES_DIR_PATH)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def handle_existing_files(watchdog_queue):
    for file in os.listdir(config.IMAGES_DIR_PATH):
        file_path = os.path.join(config.IMAGES_DIR_PATH, file)
        event = FileClosedEvent(file_path)
        watchdog_queue.put(event)


def start_multi_processing(q):
    while True:
        try:
            process_queue(q)
        except Exception:
            error_logger.error(f'the files were not sent do to: {Exception.__str__}')


def process_queue(q):
    if not q.empty():
        event = q.pop()
        arrived_logger.info(f'the file {event.src_path} has been received')
        half_file_name: str = event.src_path.split("/")[-1]
        if "_a" != half_file_name.split('.')[:-1] and "_b" != half_file_name.split('.')[:-1]:
            error_logger.error(f'the file {half_file_name} name is not in the requested format')
        else:
            whole_file_name = half_file_name.split("_")[0]
            handle_file(half_file_name, whole_file_name)


class Handler(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_closed(self, event):
        self.queue.put(event)


def handle_file(half_file_name, whole_file_name):
    if Redis.check_existence(whole_file_name):
        first_half = Redis.extract(whole_file_name)
        second_half = half_file_name
        if second_half != first_half:
            HTTPLoad.execute([first_half, second_half])
        else:
            error_logger.warning(f'the file {half_file_name} has been sent twice')
            Redis.load(half_file_name, whole_file_name)
    else:
        Redis.load(half_file_name, whole_file_name)
