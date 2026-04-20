from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai import generate_output
from scoring import score_outputs

app = FastAPI()

# Permettre au Web App de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHALLENGE = """
OBJECTIVE:
Write a prompt that generates a high-converting sales page
for an ebook: "Learn ChatGPT in 7 days"
"""

BASELINE_PROMPT = """
Write a simple sales page for an ebook called 
'Learn ChatGPT in 7 days'.
"""

class FightRequest(BaseModel):
    user_prompt: str

@app.post("/api/fight")
async def start_fight(request: FightRequest):
    try:
        user_output = generate_output(request.user_prompt)
        baseline_output = generate_output(BASELINE_PROMPT)
        result = score_outputs(user_output, baseline_output)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
