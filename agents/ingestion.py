import uuid
from typing import List
from models import Document
from utils.logging import get_logger

logger = get_logger(__name__)

class IngestionAgent:
    def __init__(self):
        self.documents = []  # In-memory storage; replace with DB in production

    def ingest_document(self, content: str, filename: str, metadata: dict = None) -> Document:
        doc_id = str(uuid.uuid4())
        doc = Document(
            id=doc_id,
            content=content,
            filename=filename,
            metadata=metadata or {}
        )
        self.documents.append(doc)
        logger.info(f"Document ingested: {doc_id} - {filename}")
        return doc

    def get_document(self, doc_id: str) -> Document:
        for doc in self.documents:
            if doc.id == doc_id:
                return doc
        raise ValueError(f"Document {doc_id} not found")

    def list_documents(self) -> List[Document]:
        return self.documents
