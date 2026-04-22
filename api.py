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
    user_id: str = "inconnu"
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
