from abc import ABC, abstractmethod


class AbstractLoad(ABC):
    @staticmethod
    @abstractmethod
    def execute(files_names):
        pass

    @staticmethod
    @abstractmethod
    def load_files(files):
        pass
