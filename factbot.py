import os
import requests
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEBUG_CHAT_ID = os.getenv("DEBUG_CHAT_ID")

openai.api_key = OPENAI_API_KEY

def send_to_telegram(message: str, debug=False):
    chat_id = DEBUG_CHAT_ID if debug else TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("❌ Ошибка при отправке в Telegram:", e)

def main():
    print("📂 Читаем файл prompt...")
    try:
        with open("fact_prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
    except FileNotFoundError:
        send_to_telegram("❌ Не найден файл `fact_prompt.txt`", debug=True)
        return

    print("📥 Отправляем запрос в OpenAI...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=100,
            timeout=30
        )
    except Exception as e:
        send_to_telegram(f"❌ Ошибка OpenAI:\n{e}", debug=True)
        return

    try:
        fact = response["choices"][0]["message"]["content"].strip()
        print("✅ Получен факт:", fact)
        send_to_telegram(fact)
    except Exception as e:
        send_to_telegram(f"❌ Ошибка обработки ответа:\n{e}", debug=True)

if __name__ == "__main__":
    main()
