from sqlalchemy import create_engine, Column, String, DateTime, JSON, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid
from .config import settings

Base = declarative_base()

class AIRiskAssessment(Base):
    __tablename__ = "ai_risk_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    system_name = Column(String(200), nullable=False)
    system_description = Column(Text, nullable=True)
    answers = Column(JSON, nullable=False)
    classification = Column(String(50), nullable=False)
    classification_score = Column(Float, nullable=True)
    compliance_gaps = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    draft_version = Column(String(50), default=settings.draft_version)
    report_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
