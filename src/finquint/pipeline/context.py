from dataclasses import dataclass, field
from typing import Any

@dataclass
class PipelineContext:
    metadata: dict[str, Any] = field(default_factory=dict)
    results: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    errors: list[dict[str, Any]] = field(default_factory=list)

    def set(self, key, value):
        self.results[key] = value

    def get(self, key, default=None):
        return self.results.get(key, default)

    def add_error(self, stage, exc):
        self.errors.append({
            "stage": stage,
            "type": type(exc).__name__,
            "message": str(exc),
        })
