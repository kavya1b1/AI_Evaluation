from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import uuid
import os


def generate_report(
    filename,
    scores,
    decision,
    explanation,
    ai_narrative=None,
    confidence_data=None   # ✅ FIX: accept confidence_data
):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:6]
    final_filename = f"{timestamp}_{uid}_{filename}"
    file_path = os.path.join("reports", final_filename)

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # ---------------- TITLE ----------------
    story.append(Paragraph(
        "<b>AI-Based R&D Proposal Evaluation Report</b>",
        styles["Title"]
    ))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    # ---------------- SCORES TABLE ----------------
    story.append(Paragraph("<b>ML-Based Evaluation Scores</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    table_data = [
        ["Metric", "Score"],
        ["Novelty Score", f"{scores['novelty']:.2f}"],
        ["Financial Compliance", f"{scores['finance']:.2f}"],
        ["Final AI Score", f"{scores['final_score']:.2f}"],
    ]

    table = Table(table_data, colWidths=[220, 120])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
        ("FONT", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (-1,-1), "CENTER")
    ]))

    story.append(table)
    story.append(Spacer(1, 16))

    # ---------------- DECISION ----------------
    story.append(Paragraph("<b>Funding Recommendation</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(decision, styles["Normal"]))
    story.append(Spacer(1, 16))

    # ---------------- XAI ----------------
    story.append(Paragraph("<b>Explainable AI Insights</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))
    for point in explanation:
        story.append(Paragraph(f"• {point}", styles["Normal"]))
    story.append(Spacer(1, 16))

    # ---------------- CONFIDENCE & UNCERTAINTY ----------------
    if confidence_data:
        mean = confidence_data["mean"]
        lower = confidence_data["lower"]
        upper = confidence_data["upper"]
        confidence = confidence_data["confidence"]

        story.append(Paragraph("<b>Model Confidence & Risk</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f"""
            Final Score (Mean): <b>{mean:.2f}</b><br/>
            Confidence Interval: <b>{lower:.2f} – {upper:.2f}</b><br/>
            Model Confidence: <b>{confidence:.2f}%</b>
            """,
            styles["Normal"]
        ))
        story.append(Spacer(1, 16))

    # ---------------- GENAI NARRATIVE ----------------
    if ai_narrative:
        story.append(Paragraph("<b>AI-Generated Evaluation Narrative</b>", styles["Heading2"]))
        story.append(Spacer(1, 8))
        story.append(Paragraph(ai_narrative, styles["Normal"]))
        story.append(Spacer(1, 20))

    # ---------------- FOOTER ----------------
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<i>This report was automatically generated using Machine Learning, "
        "Explainable AI, and Generative AI models. Human review is recommended.</i>",
        styles["Italic"]
    ))

    doc.build(story)

    return final_filename, file_path
