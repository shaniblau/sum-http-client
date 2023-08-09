from redis import Redis as RedisClient
from .abstract_db import AbstractDB
from configuration import config


redis_client = RedisClient(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)


class Redis(AbstractDB):
    @staticmethod
    def check_existence(file_full_name):
        return redis_client.exists(file_full_name)

    @staticmethod
    def load(file_name, file_full_name):
        redis_client.set(file_full_name, file_name)
        redis_client.expire(file_full_name, config.DEL_TIME)

    @staticmethod
    def extract(file_full_name):
        first_half = redis_client.get(file_full_name)
        redis_client.delete(file_full_name)
        return first_half
