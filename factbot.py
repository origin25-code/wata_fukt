import os
import openai
import requests
import sys
from datetime import datetime

# 🔍 Логируем и проверяем переменные окружения
def check_env(key):
    value = os.getenv(key)
    if not value:
        print(f"⛔ Переменная {key} не найдена")
        sys.exit(1)
    print(f"✅ {key} найден: {value[:5]}...")
    return value

OPENAI_API_KEY = check_env("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = check_env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = check_env("TELEGRAM_CHAT_ID")
DEBUG_CHAT_ID = os.getenv("DEBUG_CHAT_ID") or TELEGRAM_CHAT_ID

openai.api_key = OPENAI_API_KEY

# 🧠 Загружаем промпт из файла
try:
    with open("fact_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
except FileNotFoundError:
    print("⛔ Файл fact_prompt.txt не найден")
    sys.exit(1)

print("📥 Промпт загружен:")
print(prompt[:80], "...")

# 🧠 Запрос к OpenAI
print("🚀 Отправляем запрос к OpenAI...")
try:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Дай один факт."}
        ],
        max_tokens=100,
        temperature=0.9,
    )
except Exception as e:
    print("⛔ Ошибка OpenAI:", str(e))
    sys.exit(1)

fact = response['choices'][0]['message']['content'].strip()
print("🧠 Факт получен:")
print(fact)

# 📤 Отправка в Telegram
def send_telegram(message: str, chat_id: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    r = requests.post(url, data=data)
    if not r.ok:
        print(f"⛔ Ошибка Telegram: {r.status_code} — {r.text}")
        sys.exit(1)
    print(f"✅ Успешно отправлено в чат {chat_id}")

# 🔁 Отправляем факт
send_telegram(fact, TELEGRAM_CHAT_ID)

# 🪵 Лог-фраза в DEBUG чат
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
send_telegram(f"🛠️ factbot.py завершён в {timestamp}", DEBUG_CHAT_ID)
