import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.telegram import TelegramWebAppInfo

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    
    # LE BOUTON MAGIQUE QUI OUVRE L'INTERFACE WEB
    builder.button(
        text="🚀 Ouvrir Prompt Arena", 
        web_app=TelegramWebAppInfo(url="https://observed-nova-quality-cake.trycloudflare.com") # <--- REMPLACE ICI
    )
    
    await message.answer(
        "⚡ **Prompt Fight Arena** ⚡\n\n"
        "Le bot a évolué ! Clique sur le bouton ci-dessous pour accéder à l'arène interactive.",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

async def main():
    print("Bot démarré !")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
