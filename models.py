from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Document(BaseModel):
    id: str
    content: str
    filename: str
    uploaded_at: datetime = datetime.utcnow()
    metadata: Optional[Dict[str, Any]] = {}

class ExtractedData(BaseModel):
    document_id: str
    dates: List[str] = []
    metrics: Dict[str, Any] = {}
    obligations: List[str] = []
    entities: List[str] = []

class Summary(BaseModel):
    document_id: str
    summary_text: str
    key_points: List[str] = []
    generated_at: datetime = datetime.utcnow()

class Insight(BaseModel):
    document_id: str
    insights: List[str] = []
    recommendations: List[str] = []
    generated_at: datetime = datetime.utcnow()

class ComplianceCheck(BaseModel):
    document_id: str
    risks: List[str] = []
    compliance_status: str  # e.g., "Compliant", "Non-Compliant"
    audit_trail: List[str] = []
    checked_at: datetime = datetime.utcnow()

class BlogPost(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    generated_at: datetime = datetime.utcnow()
    based_on_document_ids: List[str] = []

class User(BaseModel):
    username: str
    email: str
    role: str  # e.g., "admin", "user"
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
