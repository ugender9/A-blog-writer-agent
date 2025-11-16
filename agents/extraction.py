import re
from typing import Dict, Any, List
from models import ExtractedData
from utils.logging import get_logger

logger = get_logger(__name__)

class ExtractionAgent:
    def __init__(self):
        pass

    def extract_data(self, document_content: str, document_id: str) -> ExtractedData:
        dates = self._extract_dates(document_content)
        metrics = self._extract_metrics(document_content)
        obligations = self._extract_obligations(document_content)
        entities = self._extract_entities(document_content)

        extracted = ExtractedData(
            document_id=document_id,
            dates=dates,
            metrics=metrics,
            obligations=obligations,
            entities=entities
        )
        logger.info(f"Data extracted for document: {document_id}")
        return extracted

    def _extract_dates(self, text: str) -> List[str]:
        # Simple regex for dates (e.g., DD/MM/YYYY, MM/DD/YYYY)
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        return re.findall(date_pattern, text)

    def _extract_metrics(self, text: str) -> Dict[str, Any]:
        # Extract numbers that might be metrics (e.g., $100, 50%, 1.5M)
        metric_pattern = r'\b\d+(\.\d+)?[KMB%\$]?\b'
        metrics = re.findall(metric_pattern, text)
        return {"potential_metrics": metrics}

    def _extract_obligations(self, text: str) -> List[str]:
        # Look for sentences with obligation keywords
        obligation_keywords = ['must', 'shall', 'required', 'obligated', 'deadline']
        sentences = re.split(r'[.!?]', text)
        obligations = [s.strip() for s in sentences if any(kw in s.lower() for kw in obligation_keywords)]
        return obligations

    def _extract_entities(self, text: str) -> List[str]:
        # Simple entity extraction (proper nouns, capitalized words)
        entity_pattern = r'\b[A-Z][a-z]+\b'
        entities = re.findall(entity_pattern, text)
        return list(set(entities))  # Unique entities
