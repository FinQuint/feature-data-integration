from abc import ABC, abstractmethod
from .dataset import QuantDataset

class DataProvider(ABC):
    source_type = "unknown"

    @abstractmethod
    def load(self) -> QuantDataset:
        raise NotImplementedError
