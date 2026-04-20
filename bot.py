import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import BOT_TOKEN
from ai import generate_output
from scoring import score_outputs

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_state = {}

CHALLENGE = """
OBJECTIVE:
Write a prompt that generates a high-converting sales page
for an ebook: "Learn ChatGPT in 7 days"
"""

BASELINE_PROMPT = """
Write a simple sales page for an ebook called 
'Learn ChatGPT in 7 days'.
"""

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🔥 Prompt Fight Arena\n\n"
        "Use /fight to start."
    )

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

    await message.answer(f"🔥 RESULT:\n\n{result}")

    user_state[message.from_user.id] = None

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
