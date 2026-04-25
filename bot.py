import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # Le bot lit l'URL écrite par le script start.sh
    try:
        with open("/tmp/tunnel_url.txt", "r") as f:
            base_url = f.read().strip()
    except FileNotFoundError:
        base_url = "https://error.trycloudflare.com"

    kb = [
        # On construit les liens dynamiquement ici ! Plus de placeholders !
        [InlineKeyboardButton(text="⚔️ Arena (Fight)", web_app=WebAppInfo(url=f"{base_url}/index.html"))],
        [InlineKeyboardButton(text="💡 AI Coach", web_app=WebAppInfo(url=f"{base_url}/coach.html"))]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer(
        "⚡ **Prompt Fight Arena** ⚡\n\nChoisis un mode :",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def main():
    print("Bot démarré avec succès !")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
