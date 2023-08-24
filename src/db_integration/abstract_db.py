from abc import ABC, abstractmethod


class AbstractDB(ABC):

    @staticmethod
    @abstractmethod
    def load(file_name, file_full_name):
        pass

    @staticmethod
    @abstractmethod
    def extract(file_full_name):
        pass
