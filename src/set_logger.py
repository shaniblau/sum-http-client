import logging as log


def extendable_logger(file_path, level):
    specified_logger = log.getLogger('app.py')
    specified_logger.setLevel(level)
    handler = log.FileHandler(file_path)
    formatter = log.Formatter('{"logging.level":"%(levelname)s","message":"%(message)s"}')
    handler.setFormatter(formatter)
    specified_logger.addHandler(handler)
    return specified_logger
