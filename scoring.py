import requests
from config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

MODEL = "openai/gpt-4o-mini"

# Les consignes de base
CHALLENGE = """
OBJECTIVE:
Write a prompt that generates a high-converting sales page
for an ebook: "Learn ChatGPT in 7 days"
"""

BASELINE_PROMPT = """
Write a simple sales page for an ebook called 
'Learn ChatGPT in 7 days'.
"""

def score_outputs(user_prompt: str, user_output: str, baseline_output: str) -> str:
    prompt = f"""
    You are a ruthless and highly accurate AI Copywriting Judge.
    
    CONTEXT:
    - The Original Challenge/Objective was: "{CHALLENGE}"
    
    PROMPTS SUBMITTED:
    - Prompt A (User's Prompt): "{user_prompt}"
    - Prompt B (Baseline Prompt): "{BASELINE_PROMPT}"
    
    GENERATED OUTPUTS:
    - Output A (Generated from User Prompt): 
    {user_output}
    
    - Output B (Generated from Baseline Prompt): 
    {baseline_output}
    
    YOUR MISSION:
    Evaluate how well the GENERATED OUTPUTS fulfilled the ORIGINAL CHALLENGE. A good output must perfectly match the objective, be highly persuasive, and well-structured.
    
    SCORING CRITERIA (0-20 each):
    1. Relevance to Challenge: Does it actually sell the ChatGPT ebook?
    2. Persuasion: Is it high-converting? (Call to action, urgency, benefits)
    3. Structure: Is it readable? (Headings, bullet points, spacing)
    4. Originality: Is it creative or just a boring generic text?
    5. Prompt Efficiency: Did the specific prompt yield a better result than the baseline?
    
    OUTPUT FORMAT (STRICT):
    Score A: X/100
    Score B: X/100
    Winner: A or B
    
    Explanation:
    [Explain why the winner is better based on the challenge context]
    
    Improvements for the loser:
    1. [First actionable improvement for the text/prompt]
    2. [Second actionable improvement for the text/prompt]
    """

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2 # Température basse pour un jugement plus logique et moins créatif
    }

    response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]
