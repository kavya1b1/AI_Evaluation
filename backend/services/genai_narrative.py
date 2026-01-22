import os
from openai import OpenAI

# Load OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY environment variable is not set"
    )

# OpenRouter uses OpenAI-compatible client
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Choose model (can be changed anytime)
MODEL_NAME = "mistralai/mistral-7b-instruct"

def generate_ai_narrative(
    proposal_text: str,
    novelty: float,
    finance: float,
    final_score: float,
    decision: str
) -> str:
    """
    Generates a professional AI-written evaluation narrative
    using an LLM accessed via OpenRouter.
    """

    prompt = f"""
You are a senior R&D evaluator for a government research organization.

Write a professional evaluation narrative (200–300 words)
for the following research proposal.

Proposal Summary:
{proposal_text[:1500]}

Evaluation Signals:
- Novelty Score: {novelty}
- Financial Compliance Score: {finance}
- Final AI Score: {final_score}
- Funding Decision: {decision}

Your evaluation MUST cover:
1. Technical strengths
2. Innovation and novelty
3. Feasibility and risks
4. Final funding recommendation

Use formal, objective, expert-level language.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
