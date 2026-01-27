import os
from openai import OpenAI

# ✅ OpenRouter Setup
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "mistralai/mixtral-8x7b-instruct"


def reviewer_chat_response(question, proposal_text, evaluation_summary):

    prompt = f"""
You are a funding proposal reviewer agent.

Proposal Text:
{proposal_text[:1500]}

Evaluation Summary:
{evaluation_summary}

User Question:
{question}

Answer clearly in 5–6 lines like a reviewer.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
