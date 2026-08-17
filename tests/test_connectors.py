import pandas as pd
from finquint.data.connectors import CSVProvider, JSONProvider, ParquetProvider

def test_csv(tmp_path):
    p = tmp_path / "a.csv"
    pd.DataFrame({"x":[1,2]}).to_csv(p,index=False)
    assert CSVProvider(p).load().row_count == 2

def test_json(tmp_path):
    p = tmp_path / "a.json"
    pd.DataFrame({"x":[1,2]}).to_json(p,orient="records")
    assert JSONProvider(p).load().row_count == 2

def test_parquet(tmp_path):
    p = tmp_path / "a.parquet"
    pd.DataFrame({"x":[1,2]}).to_parquet(p,index=False)
    assert ParquetProvider(p).load().row_count == 2
