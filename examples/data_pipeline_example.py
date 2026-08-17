from pathlib import Path
import pandas as pd
from finquint.data import SchemaRules
from finquint.data.connectors import CSVProvider
from finquint.pipeline import QuantPipeline
from finquint.pipeline.stages import LoadDataStage, NormalizeDataStage, ValidateDataStage

sample = Path("data/raw/sample.csv")
sample.parent.mkdir(parents=True, exist_ok=True)
if not sample.exists():
    pd.DataFrame({
        "Instrument ID": ["UST2Y", "UST5Y", "UST10Y"],
        "Yield": ["0.041", "0.043", "0.045"],
    }).to_csv(sample, index=False)

rules = SchemaRules(
    required_columns=["instrument_id", "yield"],
    unique_columns=["instrument_id"],
    ranges={"yield": {"minimum": -0.10, "maximum": 1.0}},
)

pipeline = (
    QuantPipeline(name="market_data_example")
    .add(LoadDataStage(CSVProvider(sample)))
    .add(NormalizeDataStage(dtypes={"instrument_id": "string", "yield": "float"}))
    .add(ValidateDataStage(rules))
)

dataset = pipeline.run()
print(dataset.data)
print(pipeline.last_context.metadata)
print(pipeline.last_context.metrics)
