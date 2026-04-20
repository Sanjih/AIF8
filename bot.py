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
# Dictionnaire temporaire pour les scores (sera remplacé par une BDD plus tard)
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
# 1. MENU PRINCIPAL (Clavier)
# ==========================================
def home_keyboard():
    kb = [
        # Bouton principal mis en valeur
        [InlineKeyboardButton(text="🚀 Enter the Arena", callback_data="menu_fight")],
        
        # Boutons secondaires sur la même ligne
        [
            InlineKeyboardButton(text="📊 My Stats", callback_data="menu_stats"),
            InlineKeyboardButton(text="🏆 Leaderboard", callback_data="menu_leaderboard")
        ],
        
        # Bouton défi quotidien
        [InlineKeyboardButton(text="📅 Daily Challenge", callback_data="menu_daily")],
        
        # Bouton qui ouvre un lien web externe (Style ChainGPT)
        [InlineKeyboardButton(text="🌐 Web Version", url="https://REMPLACE_PAR_TON_SITE.com")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# ==========================================
# 2. /start (HOME STYLE CHAINGPT)
# ==========================================
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    score = user_scores.get(user_id, 0)
    
    # METS L'URL DE TA BANNIERE ICI (image hightech de 1200x600px)
    BANNER_URL = "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200" 
    
    # Texte formaté sous l'image
    caption_text = (
        f"⚡ **PROMPT FIGHT ARENA IS LIVE** ⚡\n\n"
        f"Welcome to the most advanced AI Prompt Battleground on Telegram.\n\n"
        f"🔥 *What you can do:*\n"
        f"▪️ Battle against AI baselines\n"
        f"▪️ Improve your copywriting skills\n"
        f"▪️ Climb the Global Leaderboard\n\n"
        f"👤 *Player:* {message.from_user.first_name}\n"
        f"💎 *Current Score:* {score} pts\n\n"
        f"_Tap a button below to begin._"
    )
    
    # Envoi de la photo + texte + boutons
    await message.answer_photo(
        photo=BANNER_URL,
        caption=caption_text,
        reply_markup=home_keyboard(),
        parse_mode="Markdown"
    )


# ==========================================
# 3. COMBAT (Gestion des commandes et textes)
# ==========================================
@dp.message(Command("fight"))
async def fight(message: types.Message):
    user_state[message.from_user.id] = "waiting_prompt"
    await message.answer(CHALLENGE)

@dp.message()
async def handle_prompt(message: types.Message):
    # On ignore si le joueur n'est pas en train de faire un combat
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

    # Mise à jour du score temporaire
    user_id = message.from_user.id
    user_scores[user_id] = user_scores.get(user_id, 0) + 10 
    
    await message.answer(
        f"🔥 RESULT:\n\n{result}\n\n🏆 *+10 points earned !*\nTap /start to return to menu.", 
        parse_mode="Markdown"
    )

    # Fin du combat
    user_state[message.from_user.id] = None


# ==========================================
# 4. CALLBACKS (Navigation des boutons)
# ==========================================
@dp.callback_query(F.data == "menu_fight")
async def callback_fight(callback: types.CallbackQuery):
    # On supprime le message avec la bannière pour libérer l'écran du téléphone
    await callback.message.delete()
    user_state[callback.from_user.id] = "waiting_prompt"
    await callback.message.answer(CHALLENGE)
    await callback.answer()

@dp.callback_query(F.data == "menu_stats")
async def callback_stats(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    score = user_scores.get(user_id, 0)
    
    text = (
        f"📊 **Your Stats**\n\n"
        f"Total Points: **{score} pts**\n"
        f"Fights Played: *Coming soon*\n"
        f"Win Rate: *Coming soon*"
    )
    # edit_text modifie le texte sans effacer les boutons
    await callback.message.edit_text(text, reply_markup=home_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_leaderboard")
async def callback_leaderboard(callback: types.CallbackQuery):
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
        f"*Use the 🚀 Enter the Arena button to submit your prompt for this challenge!*"
    )
    await callback.message.edit_text(text, reply_markup=home_keyboard(), parse_mode="Markdown")
    await callback.answer()


# ==========================================
# 5. LANCEMENT DU BOT
# ==========================================
async def main():
    print("Bot démarré avec succès !")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
