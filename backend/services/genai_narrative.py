import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

def generate_ai_narrative(
    proposal_text: str,
    novelty: float,
    finance: float,
    final_score: float,
    decision: str
):
    prompt = f"""
You are an expert research evaluator for government-funded innovation projects.

Analyze the proposal and write a professional evaluation narrative.

Proposal Summary:
{proposal_text[:2000]}

Scores:
- Novelty: {novelty}/100
- Financial Feasibility: {finance}/100
- Final AI Score: {final_score}/100

Decision: {decision}

Write a concise but authoritative evaluation narrative suitable
for a government funding committee.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI Proposal Evaluation System"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "max_tokens": 400
        }
    )

    if response.status_code != 200:
        return "AI narrative generation failed."

    return response.json()["choices"][0]["message"]["content"]

