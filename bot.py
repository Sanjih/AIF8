import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [
        [InlineKeyboardButton(
            text="🚀 Ouvrir Prompt Arena", 
            web_app=WebAppInfo(url="https://upload-para-visual-children.trycloudflare.com") # <--- METS TON VRAI LIEN ICI
        )]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer(
        "⚡ **Prompt Fight Arena** ⚡\n\n"
        "Le bot a évolué ! Clique sur le bouton ci-dessous pour accéder à l'arène interactive.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def main():
    print("Bot démarré avec succès !")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
