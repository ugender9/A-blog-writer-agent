from typing import List
from models import ComplianceCheck
from utils.logging import get_logger

logger = get_logger(__name__)

class ComplianceAgent:
    def __init__(self):
        # Define simple rules; in production, load from config or DB
        self.risk_keywords = ['breach', 'violation', 'penalty', 'non-compliance', 'risk']
        self.compliance_rules = ['Must comply with GDPR', 'Deadline must be met']

    def check_compliance(self, document_content: str, document_id: str) -> ComplianceCheck:
        risks = []
        audit_trail = []

        # Check for risk keywords
        for kw in self.risk_keywords:
            if kw.lower() in document_content.lower():
                risks.append(f"Potential risk: {kw} mentioned")
                audit_trail.append(f"Keyword '{kw}' detected")

        # Check against rules
        compliance_status = "Compliant"
        for rule in self.compliance_rules:
            if rule.lower() not in document_content.lower():
                compliance_status = "Non-Compliant"
                risks.append(f"Rule not satisfied: {rule}")
                audit_trail.append(f"Rule check failed: {rule}")

        check = ComplianceCheck(
            document_id=document_id,
            risks=risks,
            compliance_status=compliance_status,
            audit_trail=audit_trail
        )
        logger.info(f"Compliance check completed for document: {document_id} - Status: {compliance_status}")
        return check
