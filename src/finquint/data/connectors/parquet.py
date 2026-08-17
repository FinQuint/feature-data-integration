from pathlib import Path
import pandas as pd
from ..dataset import QuantDataset
from ..interfaces import DataProvider

class ParquetProvider(DataProvider):
    source_type = "parquet"

    def __init__(self, path, **kwargs):
        self.path = Path(path)
        self.kwargs = kwargs

    def load(self):
        df = pd.read_parquet(self.path, **self.kwargs)
        return QuantDataset(df, {
            "source_type": self.source_type,
            "source_path": str(self.path),
            "rows_loaded": len(df),
        })
