from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import os

from backend.services.document_parser import extract_text_from_pdf
from backend.services.novelty_engine import novelty_score
from backend.services.financial_checker import check_finance
from backend.services.explainability import generate_explanation
from backend.services.report_generator import generate_report
from backend.services.ml_evaluator import ml_evaluate
from backend.services.ml_explainability import get_feature_importance
from backend.services.uncertainty import estimate_confidence

from backend.database import get_db
from backend.models import ProposalEvaluation

router = APIRouter()


@router.post("/submit/")
async def submit_proposal(
    file: UploadFile = File(...),
    budget: float = Form(...),
    db: Session = Depends(get_db)
):
    # ------------------ Save uploaded file ------------------
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ------------------ Extract text ------------------
    text = extract_text_from_pdf(file_path)

    # ------------------ AI / ML Evaluation ------------------
    novelty = float(novelty_score(text))
    finance = float(check_finance(budget))
    technical = 80.0  # kept for explanation consistency

    score = float(ml_evaluate(text, novelty, budget))
    confidence = float(estimate_confidence(text, novelty, budget))

    # ------------------ Decision Logic ------------------
    if score >= 85:
        decision = "Strongly Recommended for Funding"
    elif score >= 70:
        decision = "Recommended with Minor Revisions"
    else:
        decision = "Not Recommended"

    # ------------------ Explainable AI ------------------
    explanation = generate_explanation(novelty, finance, technical)
    feature_importance = get_feature_importance()

    # ------------------ Generate PDF Report ------------------
    report_path = generate_report(
        filename=f"{file.filename}_evaluation.pdf",
        scores={
            "novelty": novelty,
            "finance": finance,
            "final_score": score
        },
        decision=decision,
        explanation=explanation
    )

    # ------------------ Store in Database ------------------
    record = ProposalEvaluation(
        filename=file.filename,
        novelty=novelty,
        finance=finance,
        final_score=score,
        decision=decision,
        report_path=report_path
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    # ------------------ API Response ------------------
    return {
        "novelty": novelty,
        "finance": finance,
        "final_score": score,
        "confidence": confidence,
        "decision": decision,
        "explanation": explanation,
        "feature_importance": feature_importance,
        "report_url": f"http://localhost:8000/reports/{os.path.basename(report_path)}"
    }
