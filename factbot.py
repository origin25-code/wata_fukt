import os
import openai
from dotenv import load_dotenv
from telegram import Bot

# Загрузка переменных окружения
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Новый клиент OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Загрузка промпта из файла
with open("fact_prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read().strip()

print("🧠 Генерация факта...")
try:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты — генератор шокирующих коротких фактов"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=120
    )
    fact = completion.choices[0].message.content.strip()
    print("✅ Факт: ", fact)

    # Отправка в Telegram
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=fact)
    print("📬 Отправлено в Telegram.")

except Exception as e:
    print("❌ Ошибка генерации или отправки:\n", e)
