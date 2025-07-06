import os
import openai
import requests

print("✅ Запуск factbot.py")

# Загрузка переменных среды
api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
debug_id = os.getenv("DEBUG_CHAT_ID")

if not all([api_key, bot_token, chat_id]):
    raise Exception("❌ Не найдены переменные окружения")

openai.api_key = api_key
print("🔑 OpenAI ключ загружен")

# Загрузка промпта
prompt_path = "fact_prompt.txt"
if not os.path.exists(prompt_path):
    raise FileNotFoundError(f"❌ Не найден файл: {prompt_path}")

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

print("📄 Промпт загружен")

# Генерация поста
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9,
    max_tokens=500
)
text = response["choices"][0]["message"]["content"].strip()
print("🧠 Факт сгенерирован")

# Отправка в Telegram
def send_to_telegram(msg, to_chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": to_chat_id, "text": msg}
    r = requests.post(url, json=payload)
    if not r.ok:
        raise Exception(f"❌ Ошибка отправки в Telegram: {r.text}")
    print(f"📤 Отправлено в {to_chat_id}")

send_to_telegram(text, chat_id)
send_to_telegram("✅ Пост успешно опубликован", debug_id or chat_id)

print("🎉 Готово")
