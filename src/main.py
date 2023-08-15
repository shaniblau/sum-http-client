import os
from multiprocessing import Pool
import time
from watchdog.events import FileClosedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from app import process_file
from configuration import config

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


class Handler(FileSystemEventHandler):
    def on_closed(self, event):
        pool.apply_async(process_file, (event.src_path,))


def handle_existing_files():
    for file in os.listdir(config.IMAGES_DIR_PATH):
        file_path = os.path.join(config.IMAGES_DIR_PATH, file)
        event = FileClosedEvent(file_path)
        pool.apply_async(process_file, (event.src_path,))


if __name__ == '__main__':
    run()
