import logging as log


def extendable_logger(name, file_path, level):
    specified_logger = log.getLogger(name)
    specified_logger.setLevel(level)
    handler = log.FileHandler(file_path)
    formatter = log.Formatter('{"logging.level":"%(levelname)s","message":"%(message)s"}')
    handler.setFormatter(formatter)
    specified_logger.addHandler(handler)
    return specified_logger
