from finquint.pipeline.base import PipelineStage

class LoadDataStage(PipelineStage):
    name = "load_data"

    def __init__(self, provider):
        self.provider = provider

    def run(self, data, context):
        dataset = self.provider.load()
        context.metadata["data_source"] = dataset.metadata.copy()
        context.metrics["input_rows"] = dataset.row_count
        context.metrics["input_columns"] = dataset.column_count
        return dataset
