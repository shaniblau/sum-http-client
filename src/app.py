import logging as log
from datetime import datetime

from configuration import config
from load import HTTPLoad, error_logger
from db_integration import Redis
from set_logger import extendable_logger

date = datetime.now().strftime("%d_%m_%Y")
arrived_logger = extendable_logger('arrived',f'{config.LOGS_DIR}/files-arrived/{date}.log', log.INFO)


def process_file(file_path):
    try:
        arrived_logger.info(f'the file {file_path} has been received')
        file_name = file_path.split("/")[-1]
        check_name = extract_half_file_name_(file_name)
        if "_a" != check_name[-2:] and "_b" != check_name[-2:]:
            error_logger.error(f'the file {file_name} name is not in the requested format')
        else:
            whole_file_name = file_name.split('_')[0]
            handle_half(file_name, whole_file_name)
    except Exception as e:
        error_logger.error(f'the files were not sent do to: {e}')


def extract_half_file_name_(file_name):
    if '.' in file_name:
        return file_name.split('.')[0]
    else:
        return file_name


def handle_half(file_name, whole_file_name):
    if not Redis.check_existence(whole_file_name):
        print(file_name)
        Redis.load(file_name, whole_file_name)
    else:
        first_half = Redis.extract(whole_file_name)
        second_half = file_name
        if second_half != first_half:
            HTTPLoad.execute([first_half, second_half])
        else:
            error_logger.warning(f'the file {file_name} has been sent twice')
            Redis.load(file_name, whole_file_name)

