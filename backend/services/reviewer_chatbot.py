import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def reviewer_chat_response(question, proposal_text, evaluation_summary):
    """
    Proposal Reviewer Agent:
    Answers user questions based on proposal + evaluation results.
    """

    prompt = f"""
You are an expert R&D funding reviewer at NaCCER (Coal India Limited).

You have evaluated a research proposal with the following summary:

Evaluation Summary:
{evaluation_summary}

Proposal Content (shortened):
{proposal_text[:2000]}

Now answer the user question like a professional reviewer.

User Question:
{question}

Give clear actionable feedback in 5-7 lines.
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
        return response.json()["choices"][0]["message"]["content"]

    except:
        return "⚠️ AI Reviewer could not generate response. Please try again."
