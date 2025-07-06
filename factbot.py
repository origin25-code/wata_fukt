import os
import openai
import requests
from dotenv import load_dotenv
from pathlib import Path

# Загрузка переменных из .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEBUG_CHAT_ID = os.getenv("DEBUG_CHAT_ID") or TELEGRAM_CHAT_ID

FACT_PROMPT_FILE = "fact_prompt.txt"

# Проверки на ключи
if not all([OPENAI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    raise ValueError("Не заданы переменные окружения: проверь .env")

openai.api_key = OPENAI_API_KEY

def load_prompt():
    with open(FACT_PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def generate_fact():
    prompt = load_prompt()
    print("📥 Отправляю промпт в OpenAI...")
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=300
    )
    fact = response.choices[0].message.content.strip()
    print("✅ Получен факт от OpenAI")
    return fact

def send_to_telegram(text):
    print(f"📤 Публикую пост в канал {TELEGRAM_CHAT_ID}...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка Telegram: {response.status_code}, {response.text}")
    print("🎉 Успешно опубликовано в Telegram.")

def main():
    try:
        fact = generate_fact()
        send_to_telegram(fact)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        if DEBUG_CHAT_ID:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={"chat_id": DEBUG_CHAT_ID, "text": f"Ошибка factbot: {e}"}
                )
            except:
                pass
        raise

if __name__ == "__main__":
    main()
