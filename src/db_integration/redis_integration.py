from redis import Redis as RedisClient
from .abstract_db import AbstractDB
from configuration import config

redis_client = RedisClient(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)


class Redis(AbstractDB):
    @staticmethod
    def check_existence(whole_file_name):
        return redis_client.exists(whole_file_name)

    @staticmethod
    def load(file_name, whole_file_name):
        with redis_client.lock('redis_lock') as lock:
            redis_client.setex(whole_file_name, config.DEL_TIME, file_name)

    @staticmethod
    def extract(whole_file_name):
        first_half = redis_client.get(whole_file_name)
        redis_client.delete(whole_file_name)
        return first_half
