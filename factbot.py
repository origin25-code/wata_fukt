import os
from openai import OpenAI
from telegram import Bot
from dotenv import load_dotenv

# === Загрузка переменных среды ===
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEBUG_CHAT_ID = os.getenv("DEBUG_CHAT_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

def load_prompt():
    with open("fact_prompt.txt", "r", encoding="utf-8") as file:
        return file.read().strip()

def generate_fact():
    prompt = load_prompt()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты генератор фактов"},
            {"role": "user", "content": prompt}
        ],
        temperature=1.0
    )

    return response.choices[0].message.content.strip()

def send_to_telegram(text):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def main():
    try:
        print("🔍 Генерация факта...")
        fact = generate_fact()
        print("✅ Факт: ", fact)

        send_to_telegram(fact)
        print("📬 Отправлено в Telegram.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        if DEBUG_CHAT_ID and TELEGRAM_TOKEN:
            Bot(token=TELEGRAM_TOKEN).send_message(chat_id=DEBUG_CHAT_ID, text=f"❌ FactBot error:\n{e}")

if __name__ == "__main__":
    main()
