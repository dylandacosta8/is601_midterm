from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, a=None, b=None):
        pass

    @abstractmethod
    def help(self):
        pass
