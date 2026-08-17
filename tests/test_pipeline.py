import pytest
from finquint.pipeline import PipelineStage, QuantPipeline

class AddStage(PipelineStage):
    name = "add"
    def __init__(self, amount): self.amount = amount
    def run(self, data, context):
        context.set("last_amount", self.amount)
        return data + self.amount

class FailStage(PipelineStage):
    name = "fail"
    def run(self, data, context):
        raise RuntimeError("expected failure")

def test_pipeline_executes_in_order():
    p = QuantPipeline().add(AddStage(2)).add(AddStage(3))
    assert p.run(10) == 15

def test_pipeline_records_metrics():
    p = QuantPipeline(name="test").add(AddStage(1))
    p.run(0)
    assert p.last_context.metadata["status"] == "success"
    assert "duration_seconds" in p.last_context.metrics["add"]

def test_pipeline_captures_error():
    p = QuantPipeline().add(FailStage())
    with pytest.raises(RuntimeError):
        p.run(0)
    assert p.last_context.errors[0]["stage"] == "fail"
