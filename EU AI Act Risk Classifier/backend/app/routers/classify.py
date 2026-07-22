from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db, AIRiskAssessment
from ..models import (
    ClassificationRequest, ClassificationResponse,
    RiskTier, ComplianceGap, Question
)
from ..rules.engine import classifier
from ..rules.questions import get_questions
from ..services.report_generator import report_generator, HAS_WEASYPRINT
import os

router = APIRouter(prefix="/api/classify", tags=["eu-ai-act"])

@router.get("/questions", response_model=List[Question])
async def get_question_bank():
    return [Question(**q) for q in get_questions()]

@router.post("/", response_model=ClassificationResponse)
async def classify_system(req: ClassificationRequest, db: Session = Depends(get_db)):
    if not req.answers:
        raise HTTPException(status_code=400, detail="Answers required")

    classification, score, gaps, recommendations = classifier.classify(req.answers)

    assessment = AIRiskAssessment(
        system_name=req.system_name,
        system_description=req.system_description,
        answers=req.answers,
        classification=classification.value,
        classification_score=score,
        compliance_gaps=gaps,
        recommendations=recommendations,
        draft_version="EU-AI-Act-v1.1"
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    report_path = report_generator.generate({
        "id": assessment.id,
        "system_name": assessment.system_name,
        "system_description": assessment.system_description,
        "classification": assessment.classification,
        "classification_score": assessment.classification_score,
        "compliance_gaps": assessment.compliance_gaps,
        "recommendations": assessment.recommendations,
        "draft_version": assessment.draft_version,
        "created_at": assessment.created_at.strftime("%Y-%m-%d %H:%M UTC")
    })
    assessment.report_url = f"/api/classify/{assessment.id}/report"
    db.commit()

    return ClassificationResponse(
        id=assessment.id,
        system_name=assessment.system_name,
        system_description=assessment.system_description,
        classification=RiskTier(assessment.classification),
        classification_score=assessment.classification_score,
        compliance_gaps=[ComplianceGap(**g) for g in (assessment.compliance_gaps or [])],
        recommendations=assessment.recommendations or [],
        draft_version=assessment.draft_version,
        report_url=assessment.report_url,
        created_at=assessment.created_at
    )

@router.get("/{assessment_id}/report")
async def download_report(assessment_id: str, db: Session = Depends(get_db)):
    assessment = db.query(AIRiskAssessment).filter(AIRiskAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    pdf_path = f"reports/{assessment_id}.pdf"
    html_path = f"reports/{assessment_id}.html"

    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"EU_AI_Risk_{assessment_id[:8]}.pdf")
    elif os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html", filename=f"EU_AI_Risk_{assessment_id[:8]}.html")
    else:
        raise HTTPException(status_code=404, detail="Report not generated yet")

@router.get("/history", response_model=List[ClassificationResponse])
async def get_history(db: Session = Depends(get_db), limit: int = 20):
    assessments = db.query(AIRiskAssessment).order_by(
        AIRiskAssessment.created_at.desc()
    ).limit(limit).all()

    return [
        ClassificationResponse(
            id=a.id,
            system_name=a.system_name,
            system_description=a.system_description,
            classification=RiskTier(a.classification),
            classification_score=a.classification_score,
            compliance_gaps=[ComplianceGap(**g) for g in (a.compliance_gaps or [])],
            recommendations=a.recommendations or [],
            draft_version=a.draft_version,
            report_url=a.report_url,
            created_at=a.created_at
        ) for a in assessments
    ]
