from dataclasses import dataclass, field
from typing import Any

@dataclass
class SchemaRules:
    required_columns: list[str] = field(default_factory=list)
    unique_columns: list[str] = field(default_factory=list)
    nullable: dict[str, bool] = field(default_factory=dict)
    dtypes: dict[str, str] = field(default_factory=dict)
    ranges: dict[str, dict[str, float]] = field(default_factory=dict)
    allowed_values: dict[str, list[Any]] = field(default_factory=dict)
