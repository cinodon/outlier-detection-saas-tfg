from abc import ABC, abstractmethod


class DefaultModel(ABC):
    def __init__(self):
        self.model = None
    @abstractmethod
    def _create_model(self):
        pass
    @abstractmethod
    def execute_model(self):
        pass