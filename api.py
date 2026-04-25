from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai import generate_output
from scoring import score_outputs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASELINE_PROMPT = """
Write a simple sales page for an ebook called 
'Learn ChatGPT in 7 days'.
"""

# 🆕 On met à jour le "modèle" de données attendues
class FightRequest(BaseModel):
    user_prompt: str
    user_id: int = 0  # <-- On met "int" pour nombre au lieu de "str" pour texte
    user_name: str = "Anonyme"

@app.post("/api/fight")
async def start_fight(request: FightRequest):
    
    # 🆕 On affiche qui joue dans les logs du serveur (pour vérifier que ça marche)
    print(f"⚔️ NOUVEAU COMBAT ! Joueur : {request.user_name} (ID: {request.user_id})")
    
    try:
        user_output = generate_output(request.user_prompt)
        baseline_output = generate_output(BASELINE_PROMPT)
        
        result = score_outputs(request.user_prompt, user_output, baseline_output)
        
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------------------------------------------------------
# NOUVEAU MODULE : LE COACH (Guide Touristique)
# ---------------------------------------------------------

def ask_coach(user_idea: str) -> str:
    # 1. Le serveur lit le fichier de leçons
    try:
        with open("lecons.txt", "r", encoding="utf-8") as f:
            lecons = f.read()
    except Exception:
        lecons = "Aucune leçon disponible."

    # 2. Le prompt du "Guide Touristique"
    prompt = f"""
    Tu es un guide touristique expert en copywriting et en "Prompt Engineering".
    Voici le manuel de formation du joueur :
    ---
    {lecons}
    ---
    
    Le joueur a cette idée vague : "{user_idea}"
    
    Ta mission : En te basant STRICTEMENT sur les leçons du manuel, donne-lui 2 ou 3 phrases d'orientation ultra-courtes pour l'aider à transformer son idée en un excellent prompt. 
    Ne génère pas le texte de vente. Donne juste le conseil d'orientation.
    Sois bref et direct.
    """

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=data)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]

class CoachRequest(BaseModel):
    user_idea: str

@app.post("/api/coach")
async def coach_endpoint(request: CoachRequest):
    try:
        advice = ask_coach(request.user_idea)
        return {"success": True, "advice": advice}
    except Exception as e:
        return {"success": False, "error": str(e)}
