fimport pytest
from agents.ingestion import IngestionAgent
from agents.extraction import ExtractionAgent
from agents.summarization import SummarizationAgent
from agents.analysis import AnalysisAgent
from agents.compliance import ComplianceAgent
from agents.coordinator import CoordinatorAgent
from models import ExtractedData

def test_ingestion_agent():
    agent = IngestionAgent()
    doc = agent.ingest_document("Sample content", "test.txt")
    assert doc.content == "Sample content"
    assert doc.filename == "test.txt"

def test_extraction_agent():
    agent = ExtractionAgent()
    extracted = agent.extract_data("The deadline is 15/10/2023. Amount: $1000.", "test_id")
    assert "15/10/2023" in extracted.dates
    assert "1000" in str(extracted.metrics)

def test_compliance_agent():
    agent = ComplianceAgent()
    check = agent.check_compliance("This document mentions breach.", "test_id")
    assert "breach" in str(check.risks)

# Note: Summarization and Analysis tests require OpenAI API key; mock in production
# def test_summarization_agent():
#     agent = SummarizationAgent()
#     summary = agent.summarize("Long text here.", "test_id")
#     assert summary.summary_text

def test_coordinator_agent():
    coordinator = CoordinatorAgent()
    result = coordinator.process_document("Sample document content.", "sample.txt")
    assert "document" in result
    assert "blog_post" in result
