from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import uuid
import os

from backend.services.shap_explainer import get_shap_values
from backend.services.genai_narrative import generate_ai_narrative
from backend.services.document_parser import extract_text_from_pdf

# ✅ Correct imports
from backend.services.novelty_engine import novelty_analysis
from backend.services.financial_checker import check_finance

from backend.services.explainability import (
    generate_explanation,
    get_feature_importance
)

from backend.services.report_generator import generate_report
from backend.services.uncertainty import estimate_confidence_band
from backend.services.ml_evaluator import ml_evaluate_with_uncertainty

from backend.database import get_db
from backend.models import ProposalEvaluation

router = APIRouter()


# --------------------------------------------------
# SUBMIT PROPOSAL
# --------------------------------------------------
@router.post("/submit/")
async def submit_proposal(
    file: UploadFile = File(...),
    budget: float = Form(...),
    db: Session = Depends(get_db)
):
    # ---------- Save uploaded file ----------
    os.makedirs("uploads", exist_ok=True)

    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- Extract proposal text ----------
    text = extract_text_from_pdf(file_path)

    # ==================================================
    # 1️⃣ Novelty Benchmarking (Past Project Similarity)
    # ==================================================
    novelty_result = novelty_analysis(text)

    novelty_score = float(novelty_result["novelty_score"])
    similar_projects = novelty_result["similar_projects"]

    # ==================================================
    # 2️⃣ Financial Compliance + Rule Violations
    # ==================================================
    finance_result = check_finance(budget)

    finance_score = float(finance_result["finance_score"])
    violations = finance_result["violations"]

    technical = 80.0  # heuristic placeholder

    # ==================================================
    # 3️⃣ ML Ensemble + Uncertainty
    # ==================================================
    predictions = ml_evaluate_with_uncertainty(novelty_score, budget)

    confidence_data = estimate_confidence_band(predictions)

    final_score = float(confidence_data["mean"])
    confidence = float(confidence_data["confidence"])

    # ==================================================
    # 4️⃣ Decision Logic
    # ==================================================
    if final_score >= 85:
        decision = "Strongly Recommended for Funding"
    elif final_score >= 70:
        decision = "Recommended with Minor Revisions"
    else:
        decision = "Not Recommended"

    # ==================================================
    # 5️⃣ GenAI Narrative Report
    # ==================================================
    ai_report_text = generate_ai_narrative(
        proposal_text=text,
        novelty=novelty_score,
        finance=finance_score,
        final_score=final_score,
        decision=decision
    )

    # ==================================================
    # 6️⃣ Explainability + Feature Importance
    # ==================================================
    explanation = generate_explanation(
        novelty_score,
        finance_score,
        technical
    )

    feature_importance = get_feature_importance()

    # ==================================================
    # 7️⃣ SHAP Explanation
    # ==================================================
    shap_values = get_shap_values(
        novelty=novelty_score,
        finance=finance_score,
        technical=technical
    )

    # ==================================================
    # 8️⃣ Generate PDF Report (Updated)
    # ==================================================
    os.makedirs("reports", exist_ok=True)

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
        confidence_data=confidence_data,

        # ✅ NEW additions
        similar_projects=similar_projects,
        violations=violations
    )

    # ==================================================
    # 9️⃣ Store Evaluation in Database
    # ==================================================
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

    # ==================================================
    # ✅ API Response
    # ==================================================
    return {
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
# HISTORY ENDPOINT (FIXED)
# --------------------------------------------------
@router.get("/history/")
def get_evaluation_history(db: Session = Depends(get_db)):

    records = (
        db.query(ProposalEvaluation)
        .order_by(ProposalEvaluation.id.desc())
        .limit(20)
        .all()
    )

    return [
        {
            "filename": r.filename,
            "novelty": r.novelty,
            "finance": r.finance,
            "final_score": r.final_score,
            "decision": r.decision,
            "created_at": r.created_at.strftime("%d %b %Y, %H:%M")
        }
        for r in records
    ]
