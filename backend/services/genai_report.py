from openai import OpenAI

client = OpenAI()

def generate_ai_report(summary, novelty, score, decision):
    prompt = f"""
You are an expert R&D evaluator.

Proposal Summary:
{summary}

Novelty Score: {novelty}
Final Score: {score}
Decision: {decision}

Write a professional evaluation report covering:
1. Strengths
2. Weaknesses
3. Funding recommendation
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
