import os
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message

# Отримуємо токени з середовища (НЕ вставляємо їх у код напряму!)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

# API URL Hugging Face (Можна змінити модель, якщо потрібно)
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

# Логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def get_ai_response(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    data = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    return "Помилка генерації відповіді."

@dp.message_handler()
async def chat_with_ai(message: Message):
    user_input = message.text
    await message.answer("Генерую відповідь...")
    response = await get_ai_response(user_input)
    await message.answer(response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
