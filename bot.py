import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN
from ai import generate_output
from scoring import score_outputs

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_state = {}
# Dictionnaire temporaire pour simuler le score utilisateur (à remplacer par une vraie BDD plus tard)
user_scores = {}

CHALLENGE = """
OBJECTIVE:
Write a prompt that generates a high-converting sales page
for an ebook: "Learn ChatGPT in 7 days"
"""

BASELINE_PROMPT = """
Write a simple sales page for an ebook called 
'Learn ChatGPT in 7 days'.
"""

# ==========================================
# 2. MENU PRINCIPAL (Clavier)
# ==========================================
def home_keyboard():
    kb = [
        [InlineKeyboardButton(text="⚔️ Fight", callback_data="menu_fight")],
        [
            InlineKeyboardButton(text="📊 Stats", callback_data="menu_stats"),
            InlineKeyboardButton(text="🏆 Leaderboard", callback_data="menu_leaderboard")
        ],
        [InlineKeyboardButton(text="📅 Daily Challenge", callback_data="menu_daily")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# ==========================================
# 1. /start (HOME)
# ==========================================
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    
    # Récupérer le score (0 si nouveau joueur)
    score = user_scores.get(user_id, 0)
    
    await message.answer(
        f"🔥 **Prompt Fight Arena** 🔥\n\n"
        f"Welcome, {message.from_user.first_name}!\n"
        f"Current Score: **{score} pts**\n\n"
        f"Choose an action below:",
        reply_markup=home_keyboard(),
        parse_mode="Markdown"
    )

# ==========================================
# ANCIENNE LOGIQUE DU FIGHT ( Gardée pour compatibilité avec la commande texte )
# ==========================================
@dp.message(Command("fight"))
async def fight(message: types.Message):
    user_state[message.from_user.id] = "waiting_prompt"
    await message.answer(CHALLENGE)

@dp.message()
async def handle_prompt(message: types.Message):
    if user_state.get(message.from_user.id) != "waiting_prompt":
        return

    user_prompt = message.text
    await message.answer("⚔️ Generating outputs...")

    try:
        user_output = generate_output(user_prompt)
        baseline_output = generate_output(BASELINE_PROMPT)
    except Exception as e:
        await message.answer(f"❌ Error generating outputs: {e}")
        return

    await message.answer("📊 Scoring...")

    try:
        result = score_outputs(user_output, baseline_output)
    except Exception as e:
        await message.answer(f"❌ Error scoring: {e}")
        return

    # --- AJOUT TEMPORAIRE POUR LE SCORE ---
    user_id = message.from_user.id
    user_scores[user_id] = user_scores.get(user_id, 0) + 10 # On ajoute 10 pts par victoire pour l'exemple
    # --------------------------------------

    await message.answer(
        f"🔥 RESULT:\n\n{result}\n\n🏆 *+10 points earned !*\nTap /start to return to menu.", 
        parse_mode="Markdown"
    )

    user_state[message.from_user.id] = None


# ==========================================
# 3. CALLBACKS (Navigation)
# ==========================================
@dp.callback_query(F.data == "menu_fight")
async def callback_fight(callback: types.CallbackQuery):
    # On supprime le message du menu pour faire de la place
    await callback.message.delete()
    user_state[callback.from_user.id] = "waiting_prompt"
    await callback.message.answer(CHALLENGE)
    await callback.answer()

@dp.callback_query(F.data == "menu_stats")
async def callback_stats(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    score = user_scores.get(user_id, 0)
    
    # On modifie le message du menu pour afficher les stats (sans le supprimer)
    text = (
        f"📊 **Your Stats**\n\n"
        f"Total Points: **{score} pts**\n"
        f"Fights Played: *Coming soon*\n"
        f"Win Rate: *Coming soon*"
    )
    await callback.message.edit_text(text, reply_markup=home_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_leaderboard")
async def callback_leaderboard(callback: types.CallbackQuery):
    # Ici tu pourras connecter une vraie BDD plus tard
    text = (
        "🏆 **Global Leaderboard**\n\n"
        "1. @UserA - 150 pts\n"
        "2. @UserB - 80 pts\n"
        "3. @UserC - 40 pts\n\n"
        "*Rankings reset every Monday.*"
    )
    await callback.message.edit_text(text, reply_markup=home_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_daily")
async def callback_daily(callback: types.CallbackQuery):
    text = (
        f"📅 **Daily Challenge**\n\n{CHALLENGE}\n\n"
        f"*Use the ⚔️ Fight button to submit your prompt for this challenge!*"
    )
    await callback.message.edit_text(text, reply_markup=home_keyboard(), parse_mode="Markdown")
    await callback.answer()


# ==========================================
# LANCEMENT DU BOT
# ==========================================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
