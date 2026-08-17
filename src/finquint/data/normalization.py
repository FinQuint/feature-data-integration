import re
import numpy as np
import pandas as pd
from .dataset import QuantDataset

NULL_STRINGS = {"", "na", "n/a", "none", "null", "nan"}

def normalize_column_name(name):
    text = str(name).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")

def normalize_dataset(dataset, dtypes=None, normalize_nulls=True):
    result = dataset.copy()
    df = result.data
    df.columns = [normalize_column_name(c) for c in df.columns]

    if normalize_nulls:
        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].map(
                lambda x: np.nan if isinstance(x, str) and x.strip().lower() in NULL_STRINGS else x
            )

    for col, dtype in (dtypes or {}).items():
        if col not in df.columns:
            continue
        if dtype in {"datetime", "datetime64[ns]"}:
            df[col] = pd.to_datetime(df[col], errors="raise")
        elif dtype in {"float", "float64"}:
            df[col] = pd.to_numeric(df[col], errors="raise").astype(float)
        elif dtype in {"int", "int64"}:
            df[col] = pd.to_numeric(df[col], errors="raise").astype("Int64")
        elif dtype in {"string", "str"}:
            df[col] = df[col].astype("string")
        elif dtype in {"bool", "boolean"}:
            df[col] = df[col].astype("boolean")
        else:
            df[col] = df[col].astype(dtype)

    result.metadata["normalized"] = True
    return result
