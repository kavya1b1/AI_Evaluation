import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def reviewer_chat_response(question, proposal_text, evaluation_summary):

    if not OPENROUTER_API_KEY:
        return "❌ OpenRouter API key missing."

    prompt = f"""
You are an expert research proposal reviewer.

Proposal Summary:
{evaluation_summary}

Proposal Content:
{proposal_text}

User Question:
{question}

Answer clearly and professionally.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        return "⚠️ Reviewer could not generate response."

    return response.json()["choices"][0]["message"]["content"]
