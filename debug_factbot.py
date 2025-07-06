import os
from dotenv import load_dotenv
from telegram import Bot
import openai

# === ЗАГРУЗКА .env ===
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEBUG_CHAT_ID = os.getenv("DEBUG_CHAT_ID")

# === ПРОВЕРКА ===
print(f"🔐 OPENAI_API_KEY: {OPENAI_API_KEY[:5]}...")
print(f"🤖 TELEGRAM_BOT_TOKEN: {TELEGRAM_TOKEN[:5]}...")
print(f"📢 TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}")
print(f"🛠 DEBUG_CHAT_ID: {DEBUG_CHAT_ID}")

# === ЗАГРУЗКА PROMPT ===
with open("fact_prompt.txt", "r", encoding="utf-8") as f:
    FACT_PROMPT = f.read().strip()

# === ЗАПРОС К OPENAI ===
openai.api_key = OPENAI_API_KEY

def generate_fact():
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты генератор фактов"},
            {"role": "user", "content": FACT_PROMPT}
        ],
        temperature=1.0
    )
    return response["choices"][0]["message"]["content"].strip()

# === ОТПРАВКА В TELEGRAM ===
def send_to_telegram(text, chat_id):
    bot = Bot(token=TELEGRAM_TOKEN)
    msg = bot.send_message(chat_id=chat_id, text=text)
    print(f"📨 Sent to {chat_id} → message_id: {msg.message_id}")

# === ОСНОВНОЙ БЛОК ===
try:
    fact = generate_fact()
    print(f"\n✅ Fact generated:\n{fact}\n")
    send_to_telegram(fact, TELEGRAM_CHAT_ID)
    send_to_telegram(f"✅ Продублирован факт:\n\n{fact}", DEBUG_CHAT_ID)
except Exception as e:
    print(f"\n❌ Error:\n{e}\n")
    send_to_telegram(f"❌ Ошибка:\n{e}", DEBUG_CHAT_ID)
