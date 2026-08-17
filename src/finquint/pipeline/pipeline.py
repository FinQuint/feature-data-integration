from datetime import datetime, timezone
from time import perf_counter
from .base import PipelineStage
from .context import PipelineContext

class QuantPipeline:
    def __init__(self, name="quant_pipeline", continue_on_error=False):
        self.name = name
        self.continue_on_error = continue_on_error
        self.stages = []
        self.last_context = None

    def add(self, stage):
        if not isinstance(stage, PipelineStage):
            raise TypeError("stage must implement PipelineStage")
        self.stages.append(stage)
        return self

    def run(self, data=None, context=None):
        context = context or PipelineContext()
        self.last_context = context
        context.metadata.update({
            "pipeline_name": self.name,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "stage_count": len(self.stages),
        })
        pipeline_start = perf_counter()

        for i, stage in enumerate(self.stages):
            stage_start = perf_counter()
            status = "success"
            try:
                data = stage.run(data, context)
            except Exception as exc:
                status = "failed"
                context.add_error(stage.name, exc)
                if not self.continue_on_error:
                    context.metrics[stage.name] = {
                        "index": i,
                        "status": status,
                        "duration_seconds": perf_counter() - stage_start,
                    }
                    context.metadata["status"] = "failed"
                    context.metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
                    context.metrics["pipeline_duration_seconds"] = perf_counter() - pipeline_start
                    raise
            context.metrics[stage.name] = {
                "index": i,
                "status": status,
                "duration_seconds": perf_counter() - stage_start,
            }

        context.metadata["status"] = "completed_with_errors" if context.errors else "success"
        context.metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
        context.metrics["pipeline_duration_seconds"] = perf_counter() - pipeline_start
        return data
