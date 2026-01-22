from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "mistralai/mixtral-8x7b-instruct"  # excellent for reasoning

def generate_ai_narrative(
    proposal_text: str,
    novelty: float,
    finance: float,
    final_score: float,
    decision: str
) -> str:
    prompt = f"""
You are a senior R&D evaluation expert working for a national research funding agency.

Your task is to write a **formal evaluation narrative** for a submitted research proposal.

You MUST:
- Base your reasoning strictly on the provided scores
- Explain WHY the proposal received this evaluation
- Maintain a professional, committee-style tone
- Avoid marketing language
- Avoid speculation beyond the given information

### Evaluation Inputs
Novelty Score: {novelty:.2f}/100  
Financial Compliance Score: {finance:.2f}/100  
Final AI Score: {final_score:.2f}/100  
Funding Decision: {decision}

### Proposal Excerpt
\"\"\"
{proposal_text[:1500]}
\"\"\"

### Output Requirements
- 1–2 structured paragraphs
- Mention strengths and limitations
- Justify the funding decision clearly
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.35
    )

    return response.choices[0].message.content.strip()
