import requests
import os


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def score_sections_with_genai(sections: dict):
    """
    Uses LLM to score proposal sections like a NaCCER reviewer.
    Returns structured scores out of 100.
    """

    prompt = f"""
You are an expert R&D evaluator at NaCCER (Coal India Limited).

Evaluate each proposal section below on a scale of 0–100:

1. Objectives clarity
2. Methodology feasibility
3. Innovation strength
4. Expected industry impact
5. Risk & feasibility planning

Return ONLY JSON like:

{{
 "Objectives": 85,
 "Methodology": 72,
 "Innovation": 90,
 "Expected Impact": 80,
 "Risk & Feasibility": 65
}}

Proposal Sections:
{sections}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mixtral-8x7b",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        result = response.json()["choices"][0]["message"]["content"]
        return eval(result)

    except:
        return {
            "Objectives": 70,
            "Methodology": 70,
            "Innovation": 70,
            "Expected Impact": 70,
            "Risk & Feasibility": 70
        }
