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


def process_file(file_path):
    try:
        arrived_logger.info(f'the file {file_path} has been received')
        file_name = extract_half_file_name(file_path)
        if "_a" != file_name[-2:] and "_b" != file_name[-2:]:
            error_logger.error(f'the file {file_name} name is not in the requested format')
        else:
            whole_file_name = file_name.split('_')[0]
            handle_half(file_name, whole_file_name)
    except Exception as e:
        error_logger.error(f'the files were not sent do to: {e}')


def extract_half_file_name(file_name):
    if '.' in file_name:
        return file_name.split("/")[-1].split('.')[0]
    else:
        return file_name.split("/")[0]


def handle_half(file_name, whole_file_name):
    if Redis.check_existence(whole_file_name):
        first_half = Redis.extract(whole_file_name)
        second_half = file_name
        if second_half != first_half:
            HTTPLoad.execute([first_half, second_half])
        else:
            error_logger.warning(f'the file {file_name} has been sent twice')
            Redis.load(file_name, whole_file_name)
    else:
        Redis.load(file_name, whole_file_name)
