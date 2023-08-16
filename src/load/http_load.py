import logging as log
import os
from datetime import datetime
import requests
from configuration import config
from .abstract_load import AbstractLoad
from set_logger import extendable_logger

date = datetime.now().strftime("%d_%m_%Y")
sent_logger = extendable_logger('sent', f'{config.LOGS_DIR}/files-sent/{date}.log', log.INFO)
error_logger = extendable_logger('errors', f'{config.LOGS_DIR}/errors.log', log.WARNING)


class HTTPLoad(AbstractLoad):
    @staticmethod
    def execute(files_names):
        files = HTTPLoad.__create_files(files_names)
        response = HTTPLoad.__load_files(files)
        HTTPLoad.__log_response(response, files_names)
        HTTPLoad.__delete_files(files_names)

    @staticmethod
    def __create_files(files_names):
        files = []
        for name in files_names:
            file_path = os.path.join(config.IMAGES_DIR_PATH, name)
            with open(file_path, 'rb') as file:
                files.append(("files", (name, file.read(), "image/jpg")))
        return files

    @staticmethod
    def __load_files(files):
        response = requests.post(config.URL, files=files)
        return response

    @staticmethod
    def __log_response(response, files_names):
        if response.status_code == 200:
            sent_logger.info(f'{files_names} sent successfully')
        else:
            error_logger.error(f'{files_names} could not be sent, response status code - {response.status_code}')

    @staticmethod
    def __delete_files(files_names):
        for name in files_names:
            file_path = os.path.join(config.IMAGES_DIR_PATH, name)
            os.remove(file_path)

