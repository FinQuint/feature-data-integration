from abc import ABC, abstractmethod
from typing import Any
from .context import PipelineContext

class PipelineStage(ABC):
    name = "unnamed_stage"

    @abstractmethod
    def run(self, data: Any, context: PipelineContext) -> Any:
        raise NotImplementedError
