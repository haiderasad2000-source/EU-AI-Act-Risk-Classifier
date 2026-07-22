from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class RiskTier(str, Enum):
    UNACCEPTABLE = "Unacceptable"
    HIGH = "High"
    LIMITED = "Limited"
    MINIMAL = "Minimal"

class QuestionOption(BaseModel):
    value: str
    label: str
    weight: float = 0.0
    is_risk_trigger: bool = False

class Question(BaseModel):
    id: str
    text: str
    category: str
    options: List[QuestionOption]
    help_text: Optional[str] = None

class ClassificationRequest(BaseModel):
    system_name: str
    system_description: Optional[str] = None
    answers: Dict[str, Any]

class ComplianceGap(BaseModel):
    article: str
    requirement: str
    status: str
    severity: str
    recommendation: str

class ClassificationResponse(BaseModel):
    id: str
    system_name: str
    system_description: Optional[str]
    classification: RiskTier
    classification_score: float
    compliance_gaps: List[ComplianceGap]
    recommendations: List[str]
    draft_version: str
    report_url: Optional[str]
    created_at: datetime
