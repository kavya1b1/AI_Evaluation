from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
import uuid

def generate_report(
    filename,
    scores,
    decision,
    explanation,
    ai_narrative=None,
    confidence=None
):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:6]
    report_filename = f"{timestamp}_{uid}_{filename}"
    file_path = os.path.join("reports", report_filename)

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

    # ---------------- EXPLAINABLE AI ----------------
    story.append(Paragraph("<b>Explainable AI Insights</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    for point in explanation:
        story.append(Paragraph(f"• {point}", styles["Normal"]))

    story.append(Spacer(1, 16))

    # ---------------- CONFIDENCE ----------------
    if confidence is not None:
        story.append(Paragraph("<b>Model Confidence & Risk</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f"The model reports a confidence level of <b>{confidence:.2f}%</b> for this evaluation.",
            styles["Normal"]
        ))
        story.append(Spacer(1, 16))

    # ---------------- AI NARRATIVE ----------------
    if ai_narrative:
        story.append(Paragraph("<b>AI-Generated Evaluation Narrative</b>", styles["Heading2"]))
        story.append(Spacer(1, 8))
        story.append(Paragraph(ai_narrative, styles["Normal"]))
        story.append(Spacer(1, 20))

    # ---------------- FOOTER ----------------
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<i>This report was automatically generated using Machine Learning, Explainable AI, "
        "and Generative AI models. Human review is recommended before final funding decisions.</i>",
        styles["Italic"]
    ))

    doc.build(story)
    return file_path
