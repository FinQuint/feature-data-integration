import pandas as pd
from .schema import SchemaRules

def validate_dataset(dataset, rules: SchemaRules):
    df = dataset.data
    errors = []

    if df.columns.duplicated().any():
        errors.append("duplicate column names detected")

    for c in rules.required_columns:
        if c not in df.columns:
            errors.append(f"missing required column: {c}")

    for c in rules.unique_columns:
        if c in df.columns and df[c].duplicated().any():
            errors.append(f"column is not unique: {c}")

    for c, nullable in rules.nullable.items():
        if not nullable and c in df.columns and df[c].isna().any():
            errors.append(f"null values are not allowed in: {c}")

    for c, bounds in rules.ranges.items():
        if c not in df.columns:
            continue
        s = pd.to_numeric(df[c], errors="coerce")
        if "minimum" in bounds and (s.dropna() < bounds["minimum"]).any():
            errors.append(f"values below minimum in: {c}")
        if "maximum" in bounds and (s.dropna() > bounds["maximum"]).any():
            errors.append(f"values above maximum in: {c}")

    for c, allowed in rules.allowed_values.items():
        if c in df.columns:
            invalid = ~df[c].isna() & ~df[c].isin(allowed)
            if invalid.any():
                errors.append(f"disallowed values in: {c}")

    return errors
