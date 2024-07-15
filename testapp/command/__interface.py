from abc import ABC, abstractmethod


class CommandInterface(ABC):
    @abstractmethod
    def run(self, *args, **kwarg):
        pass
