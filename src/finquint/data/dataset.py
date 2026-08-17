from dataclasses import dataclass, field
from typing import Any
import pandas as pd

@dataclass
class QuantDataset:
    data: pd.DataFrame
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

    @property
    def row_count(self):
        return len(self.data)

    @property
    def column_count(self):
        return len(self.data.columns)

    def copy(self):
        return QuantDataset(self.data.copy(), self.metadata.copy())
