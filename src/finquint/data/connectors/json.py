from pathlib import Path
import pandas as pd
from ..dataset import QuantDataset
from ..interfaces import DataProvider

class JSONProvider(DataProvider):
    source_type = "json"

    def __init__(self, path, lines=False, **kwargs):
        self.path = Path(path)
        self.lines = lines
        self.kwargs = kwargs

    def load(self):
        df = pd.read_json(self.path, lines=self.lines, **self.kwargs)
        return QuantDataset(df, {
            "source_type": self.source_type,
            "source_path": str(self.path),
            "json_lines": self.lines,
            "rows_loaded": len(df),
        })
