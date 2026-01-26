from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import uuid
import os

from backend.services.shap_explainer import get_shap_values
from backend.services.genai_narrative import generate_ai_narrative
from backend.services.document_parser import extract_text_from_pdf

from backend.services.novelty_engine import novelty_analysis
from backend.services.financial_checker import check_finance

from backend.services.explainability import (
    generate_explanation,
    get_feature_importance
)

from backend.services.report_generator import generate_report
from backend.services.uncertainty import estimate_confidence_band
from backend.services.ml_evaluator import ml_evaluate_with_uncertainty

from backend.services.reviewer_chatbot import reviewer_chat_response

from backend.database import get_db
from backend.models import ProposalEvaluation


router = APIRouter()

# ---------------- Budget Limits ----------------
MIN_BUDGET = 100000      # ₹1 Lakh
MAX_BUDGET = 500000000   # ₹50 Crore


# --------------------------------------------------
# SUBMIT PROPOSAL
# --------------------------------------------------
@router.post("/submit/")
async def submit_proposal(
    file: UploadFile = File(...),
    budget: float = Form(...),
    db: Session = Depends(get_db)
):
    # ---------- Budget Validation ----------
    if budget < MIN_BUDGET or budget > MAX_BUDGET:
        return {
            "error": f"Budget must be between ₹{MIN_BUDGET:,} and ₹{MAX_BUDGET:,}"
        }

    # ---------- Save File ----------
    os.makedirs("uploads", exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- Extract Text ----------
    text = extract_text_from_pdf(file_path)

    # ---------- Random PDF Rejection ----------
    if len(text) < 300:
        return {
            "error": "Uploaded PDF does not appear to be a valid research proposal."
        }

    # ---------- Novelty Benchmark ----------
    novelty_result = novelty_analysis(text)
    novelty_score = float(novelty_result["novelty_score"])
    similar_projects = novelty_result["similar_projects"]

    # ---------- Financial Check ----------
    finance_result = check_finance(budget)
    finance_score = float(finance_result["finance_score"])
    violations = finance_result["violations"]

    technical = 80.0

    # ---------- ML + Confidence ----------
    predictions = ml_evaluate_with_uncertainty(novelty_score, budget)
    confidence_data = estimate_confidence_band(predictions)

    final_score = float(confidence_data["mean"])
    confidence = float(confidence_data["confidence"])

    # ---------- Decision ----------
    if final_score >= 85:
        decision = "Strongly Recommended for Funding"
    elif final_score >= 70:
        decision = "Recommended with Minor Revisions"
    else:
        decision = "Not Recommended"

    # ---------- GenAI Narrative ----------
    ai_report_text = generate_ai_narrative(
        proposal_text=text,
        novelty=novelty_score,
        finance=finance_score,
        final_score=final_score,
        decision=decision
    )

    # ---------- Explainability ----------
    explanation = generate_explanation(novelty_score, finance_score, technical)
    feature_importance = get_feature_importance()

    # ---------- SHAP ----------
    shap_values = get_shap_values(
        novelty=novelty_score,
        finance=finance_score,
        technical=technical
    )

    # ---------- PDF Report ----------
    report_filename, report_path = generate_report(
        filename="evaluation.pdf",
        scores={
            "novelty": novelty_score,
            "finance": finance_score,
            "final_score": final_score
        },
        decision=decision,
        explanation=explanation,
        ai_narrative=ai_report_text,
        confidence_data=confidence_data
    )

    # ---------- Store in DB ----------
    record = ProposalEvaluation(
        filename=file.filename,
        novelty=novelty_score,
        finance=finance_score,
        final_score=final_score,
        decision=decision,
        report_path=report_path
    )
    db.add(record)
    db.commit()

    # ---------- Response ----------
    return {
        "proposal_text": text,

        "novelty": novelty_score,
        "finance": finance_score,
        "violations": violations,
        "similar_projects": similar_projects,

        "final_score": final_score,
        "confidence": confidence,
        "confidence_band": confidence_data,

        "decision": decision,
        "explanation": explanation,
        "feature_importance": feature_importance,

        "ai_report_text": ai_report_text,
        "shap_values": shap_values,

        "report_url": f"http://localhost:8000/reports/{report_filename}"

    }


# --------------------------------------------------
# REVIEWER AGENT CHATBOT
# --------------------------------------------------
@router.post("/ask/")
async def ask_reviewer(
    question: str = Form(...),
    proposal_text: str = Form(...),
    final_score: float = Form(...),
    decision: str = Form(...)
):
    summary = f"Final Score: {final_score}, Decision: {decision}"

    answer = reviewer_chat_response(
        question=question,
        proposal_text=proposal_text,
        evaluation_summary=summary
    )

    return {"answer": answer}


# --------------------------------------------------
# HISTORY ENDPOINT
# --------------------------------------------------
@router.get("/history/")
def get_evaluation_history(db: Session = Depends(get_db)):
    records = (
        db.query(ProposalEvaluation)
        .order_by(ProposalEvaluation.id.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "filename": r.filename,
            "final_score": r.final_score,
            "decision": r.decision,
            "created_at": r.created_at.strftime("%d %b %Y, %H:%M")
        }
        for r in records
    ]
