import pandas as pd
from finquint.data import SchemaRules
from finquint.data.connectors import CSVProvider
from finquint.pipeline import QuantPipeline
from finquint.pipeline.stages import LoadDataStage, NormalizeDataStage, ValidateDataStage

def test_end_to_end_data_pipeline(tmp_path):
    path = tmp_path / "sample.csv"
    pd.DataFrame({"Record ID": ["A1", "A2"], "Value": ["10.5", "12.0"]}).to_csv(path, index=False)

    rules = SchemaRules(
        required_columns=["record_id", "value"],
        unique_columns=["record_id"],
        ranges={"value": {"minimum": 0}},
    )

    p = (
        QuantPipeline(name="data_test")
        .add(LoadDataStage(CSVProvider(path)))
        .add(NormalizeDataStage(dtypes={"record_id": "string", "value": "float"}))
        .add(ValidateDataStage(rules))
    )

    ds = p.run()
    assert list(ds.data.columns) == ["record_id", "value"]
    assert ds.row_count == 2
    assert p.last_context.metrics["validation_error_count"] == 0
