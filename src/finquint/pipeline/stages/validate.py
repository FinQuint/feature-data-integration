from finquint.data.dataset import QuantDataset
from finquint.data.schema import SchemaRules
from finquint.data.validation import validate_dataset
from finquint.pipeline.base import PipelineStage

class ValidateDataStage(PipelineStage):
    name = "validate_data"

    def __init__(self, rules=None, required_columns=None):
        self.rules = rules or SchemaRules(required_columns=required_columns or [])

    def run(self, data, context):
        if not isinstance(data, QuantDataset):
            raise TypeError("ValidateDataStage expects QuantDataset")

        errors = validate_dataset(data, self.rules)
        context.results["validation_errors"] = errors
        context.metrics["validation_error_count"] = len(errors)

        if errors:
            raise ValueError("; ".join(errors))

        context.metadata["validated"] = True
        return data
