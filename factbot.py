import os
import openai
import requests
from datetime import datetime

# === НАСТРОЙКИ ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === PROMPT ===
with open("fact_prompt.txt", "r", encoding="utf-8") as f:
    FACT_PROMPT = f.read().strip()

# === ГЕНЕРАЦИЯ ФАКТА ===
def generate_fact():
    print("🔍 Генерация факта...")
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты генератор фактов"},
            {"role": "user", "content": FACT_PROMPT}
        ],
        temperature=1.0
    )

    fact = response["choices"][0]["message"]["content"].strip()
    print("✅ Факт:", fact)
    return fact

# === ОТПРАВКА В ТЕЛЕГРАМ ===
def send_to_telegram(text):
    print("📬 Отправка в Telegram...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    print("📨 Telegram ответ:", response.status_code, response.text)
    response.raise_for_status()

# === ОСНОВНОЙ ЗАПУСК ===
def main():
    try:
        fact = generate_fact()
        send_to_telegram(fact)
        print("🎉 Успешно отправлено!")
    except Exception as e:
        print("❌ Ошибка:", e)

if __name__ == "__main__":
    main()
