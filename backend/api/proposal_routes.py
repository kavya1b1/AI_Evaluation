from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil, uuid, os

from backend.database import get_db
from backend.models import ProposalEvaluation

from backend.services.document_parser import extract_text_from_pdf
from backend.services.novelty_engine import novelty_analysis
from backend.services.financial_checker import check_finance
from backend.services.ml_evaluator import ml_evaluate_with_uncertainty
from backend.services.uncertainty import estimate_confidence_band
from backend.services.genai_narrative import generate_ai_narrative
from backend.services.explainability import generate_explanation, get_feature_importance
from backend.services.shap_explainer import get_shap_values
from backend.services.report_generator import generate_report
from backend.services.reviewer_chatbot import reviewer_chat_response


router = APIRouter()

# ✅ Store last proposal text globally (for chatbot)
LAST_PROPOSAL_TEXT = ""
LAST_SUMMARY = ""


# --------------------------------------------------
# PDF VALIDATION FUNCTION
# --------------------------------------------------
def validate_proposal(text: str):
    keywords = ["objective", "methodology", "budget", "funding", "research"]
    found = any(word in text.lower() for word in keywords)

    if not found:
        raise HTTPException(
            status_code=400,
            detail="❌ Invalid Proposal PDF. Please upload a proper research/project proposal."
        )


# --------------------------------------------------
# SUBMIT PROPOSAL
# --------------------------------------------------
@router.post("/submit/")
async def submit_proposal(
    file: UploadFile = File(...),
    budget: float = Form(...),
    db: Session = Depends(get_db)
):
    global LAST_PROPOSAL_TEXT, LAST_SUMMARY

    # ✅ Budget Constraints
    if budget < 100000 or budget > 5000000:
        raise HTTPException(
            status_code=400,
            detail="❌ Budget must be between ₹1,00,000 and ₹50,00,000"
        )

    # ---------- Save uploaded file ----------
    os.makedirs("uploads", exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- Extract proposal text ----------
    text = extract_text_from_pdf(file_path)

    # ✅ Validate proposal type
    validate_proposal(text)

    # Save proposal for chatbot
    LAST_PROPOSAL_TEXT = text

    # ---------- Novelty ----------
    novelty_result = novelty_analysis(text)
    novelty_score = float(novelty_result["novelty_score"])
    similar_projects = novelty_result["similar_projects"]

    # ---------- Finance ----------
    finance_result = check_finance(budget)
    finance_score = float(finance_result["finance_score"])
    violations = finance_result["violations"]

    technical = 80.0

    # ---------- ML + Uncertainty ----------
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

    LAST_SUMMARY = f"Final Score: {final_score:.1f}, Decision: {decision}"

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

    shap_values = get_shap_values(
        novelty=novelty_score,
        finance=finance_score,
        technical=technical
    )

    # ---------- Generate Report ----------
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

    # ---------- Store DB ----------
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
# REVIEWER AGENT FIXED
# --------------------------------------------------
@router.post("/ask/")
async def ask_reviewer(question: str = Form(...)):

    if LAST_PROPOSAL_TEXT == "":
        raise HTTPException(
            status_code=400,
            detail="❌ Please evaluate a proposal first before asking questions."
        )

    answer = reviewer_chat_response(
        question=question,
        proposal_text=LAST_PROPOSAL_TEXT,
        evaluation_summary=LAST_SUMMARY
    )

    return {"answer": answer}


# --------------------------------------------------
# HISTORY
# --------------------------------------------------
@router.get("/history/")
def get_history(db: Session = Depends(get_db)):

    records = db.query(ProposalEvaluation).order_by(
        ProposalEvaluation.id.desc()
    ).limit(10).all()

    return [
        {
            "filename": r.filename,
            "final_score": r.final_score,
            "decision": r.decision,
            "created_at": r.created_at.strftime("%d %b %Y, %H:%M")
        }
        for r in records
    ]
