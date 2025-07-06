import os
import openai
from telegram import Bot
from datetime import datetime

# === ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEBUG_CHAT_ID = os.getenv("DEBUG_CHAT_ID", TELEGRAM_CHAT_ID)

# === ПРОВЕРКА НА ПУСТЫЕ ПЕРЕМЕННЫЕ ===
def validate_env():
    missing = []
    for key, val in {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "TELEGRAM_BOT_TOKEN": TELEGRAM_TOKEN,
        "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID
    }.items():
        if not val:
            missing.append(key)
    if missing:
        raise Exception(f"❌ Отсутствуют переменные: {', '.join(missing)}")

# === ЗАГРУЗКА ПРОМПТА ===
def load_prompt():
    try:
        with open("fact_prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f"❌ Не удалось загрузить prompt: {e}")

# === ЗАПРОС К OPENAI ===
def generate_fact(prompt: str):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты генератор фактов"},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,
            timeout=30
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"❌ Ошибка генерации факта: {e}")

# === ОТПРАВКА СООБЩЕНИЯ В TELEGRAM ===
def send_to_telegram(text, chat_id=TELEGRAM_CHAT_ID):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        raise Exception(f"❌ Не удалось отправить в Telegram: {e}")

# === ОСНОВНАЯ ТОЧКА ЗАПУСКА ===
def main():
    try:
        validate_env()
        send_to_telegram("🔧 factbot стартовал", DEBUG_CHAT_ID)

        prompt = load_prompt()
        send_to_telegram("📄 Промпт загружен", DEBUG_CHAT_ID)

        fact = generate_fact(prompt)
        send_to_telegram("🧠 Факт сгенерирован", DEBUG_CHAT_ID)

        send_to_telegram(fact, TELEGRAM_CHAT_ID)
        send_to_telegram("✅ Успешно опубликован", DEBUG_CHAT_ID)
        print(f"\n✅ Отправлено в канал:\n{fact}\n")

    except Exception as e:
        error_msg = f"❌ Fallback: {e}"
        print(error_msg)
        try:
            send_to_telegram(error_msg, DEBUG_CHAT_ID)
        except:
            pass

if __name__ == "__main__":
    main()
