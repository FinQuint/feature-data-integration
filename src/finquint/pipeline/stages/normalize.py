from finquint.data.dataset import QuantDataset
from finquint.data.normalization import normalize_dataset
from finquint.pipeline.base import PipelineStage

class NormalizeDataStage(PipelineStage):
    name = "normalize_data"

    def __init__(self, dtypes=None, normalize_nulls=True):
        self.dtypes = dtypes or {}
        self.normalize_nulls = normalize_nulls

    def run(self, data, context):
        if not isinstance(data, QuantDataset):
            raise TypeError("NormalizeDataStage expects QuantDataset")
        out = normalize_dataset(data, self.dtypes, self.normalize_nulls)
        context.metadata["normalized"] = True
        return out
