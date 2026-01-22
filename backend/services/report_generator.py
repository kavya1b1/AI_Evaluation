from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

def generate_report(filename, scores, decision, explanation):
    os.makedirs("reports", exist_ok=True)
    file_path = f"reports/{filename}"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI-Based R&D Proposal Evaluation Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Evaluation Scores</b>", styles["Heading2"]))
    story.append(Paragraph(f"Novelty Score: {scores['novelty']}", styles["Normal"]))
    story.append(Paragraph(f"Financial Compliance Score: {scores['finance']}", styles["Normal"]))
    story.append(Paragraph(f"Final Score: {scores['final_score']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Decision</b>", styles["Heading2"]))
    story.append(Paragraph(decision, styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Explainable AI Insights</b>", styles["Heading2"]))
    for line in explanation:
        story.append(Paragraph(f"- {line}", styles["Normal"]))

    doc.build(story)
    return file_path
