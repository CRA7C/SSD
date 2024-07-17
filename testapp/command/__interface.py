from abc import ABC, abstractmethod


class CommandInterface(ABC):
    @abstractmethod
    def run(self, *args, **kwarg):
        pass

    @staticmethod
    @abstractmethod
    def is_valid_args(self, *args, **kwarg):
        pass
