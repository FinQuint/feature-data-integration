# FinQuint Quant Research — Phase 1 & 2

This release completes the first two infrastructure phases of the FinQuint quantitative research framework.

## Phase 1 — Pipeline Core
- `PipelineStage` contract with names
- `PipelineContext` for metadata, results, metrics, and errors
- sequential `QuantPipeline`
- per-stage timing
- structured error capture
- optional continue-on-error
- pipeline run metadata

## Phase 2 — Data Integration
- standard `QuantDataset`
- `DataProvider` abstraction
- CSV, JSON/JSONL, and Parquet providers
- load, normalize, and validate stages
- schema rules
- null/column/type normalization
- end-to-end tests

## Install
```bash
python -m pip install -e ".[dev]"
```

## Test
```bash
pytest
```

## Example
```bash
python examples/data_pipeline_example.py
```
