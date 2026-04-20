import requests
from config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

MODEL = "openai/gpt-4o-mini"

def score_outputs(user_output: str, baseline_output: str) -> str:
    prompt = f"""
You are an expert copywriting judge.

Compare:
A (User): {user_output}
B (Baseline): {baseline_output}

Criteria:
- Clarity (0-20)
- Persuasion (0-20)
- Structure (0-20)
- Originality (0-20)
- Usefulness (0-20)

Return:

Score A: X/100
Score B: X/100
Winner: A or B

Explain briefly why.
Give 2 actionable improvements.
"""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]
