from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from backend.database import Base

class ProposalEvaluation(Base):
    __tablename__ = "proposal_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    novelty = Column(Float)
    finance = Column(Float)
    final_score = Column(Float)
    decision = Column(String)
    report_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
