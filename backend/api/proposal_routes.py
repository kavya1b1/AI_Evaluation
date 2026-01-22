from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil, os, uuid

from backend.services.genai_narrative import generate_ai_narrative
from backend.services.document_parser import extract_text_from_pdf
from backend.services.novelty_engine import novelty_score
from backend.services.financial_checker import check_finance
from backend.services.explainability import generate_explanation
from backend.services.report_generator import generate_report
from backend.services.ml_explainability import get_feature_importance
from backend.services.uncertainty import estimate_confidence_band
from backend.services.ml_evaluator import ml_evaluate_with_uncertainty

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
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ------------------ Extract text ------------------
    text = extract_text_from_pdf(file_path)

    # ------------------ Core ML Signals ------------------
    novelty = float(novelty_score(text))
    finance = float(check_finance(budget))
    technical = 80.0  # heuristic / placeholder

    # ------------------ ML Ensemble + Uncertainty ------------------
    predictions = ml_evaluate_with_uncertainty(novelty, budget)
    confidence_data = estimate_confidence_band(predictions)

    final_score = confidence_data["mean"]
    confidence = confidence_data["confidence"]

    # ------------------ Decision Logic ------------------
    if final_score >= 85:
        decision = "Strongly Recommended for Funding"
    elif final_score >= 70:
        decision = "Recommended with Minor Revisions"
    else:
        decision = "Not Recommended"

    # ------------------ GenAI Narrative ------------------
    ai_report_text = generate_ai_narrative(
        proposal_text=text,
        novelty=novelty,
        finance=finance,
        final_score=final_score,
        decision=decision
    )

    # ------------------ Explainable AI ------------------
    explanation = generate_explanation(novelty, finance, technical)
    feature_importance = get_feature_importance()

    # ------------------ Generate PDF Report ------------------
    report_filename = f"{file_id}_evaluation.pdf"

    report_path = generate_report(
        filename=report_filename,
        scores={
            "novelty": novelty,
            "finance": finance,
            "final_score": final_score
        },
        decision=decision,
        explanation=explanation,
        ai_narrative=ai_report_text,
        confidence_data=confidence_data
    )

    # ------------------ Store in Database ------------------
    record = ProposalEvaluation(
        filename=file.filename,
        novelty=novelty,
        finance=finance,
        final_score=final_score,
        decision=decision,
        report_path=report_path
    )

    db.add(record)
    db.commit()

    # ------------------ API Response ------------------
    return {
        "novelty": novelty,
        "finance": finance,
        "final_score": final_score,
        "confidence": confidence,
        "confidence_band": confidence_data,
        "decision": decision,
        "explanation": explanation,
        "feature_importance": feature_importance,
        "ai_report_text": ai_report_text,
        "report_url": f"http://localhost:8000/reports/{report_filename}"
    }
