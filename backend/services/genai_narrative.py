import os
from openai import OpenAI

# ✅ OpenRouter Config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "mistralai/mixtral-8x7b-instruct"


def generate_ai_narrative(proposal_text, novelty, finance, final_score, decision):

    prompt = f"""
You are an expert research funding reviewer.

Proposal Summary:
{proposal_text[:1500]}

Evaluation Scores:
- Novelty Score: {novelty:.2f}
- Finance Score: {finance:.2f}
- Final Score: {final_score:.2f}

Decision: {decision}

Write a professional evaluation narrative in 8–10 lines.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
