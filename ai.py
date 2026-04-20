import requests
from config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

MODEL = "openai/gpt-4o-mini"  # tu peux changer plus tard

def generate_output(prompt: str) -> str:
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a high-level copywriter."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]
