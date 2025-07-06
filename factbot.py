import os
from openai import OpenAI
import requests

# Промпт из файла
with open("fact_prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read().strip()

# Загружаем переменные окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверка токенов
if not all([OPENAI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    raise ValueError("⛔ Не все переменные окружения заданы")

print("🔑 OPENAI_API_KEY найден:", OPENAI_API_KEY[:5], "...")
print("🤖 TELEGRAM_BOT_TOKEN найден:", TELEGRAM_BOT_TOKEN[:5], "...")
print("💬 TELEGRAM_CHAT_ID найден:", TELEGRAM_CHAT_ID)

# Создаём клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Получаем факт
print("🚀 Отправляем запрос к OpenAI...")
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
)
fact = completion.choices[0].message.content.strip()

print("📤 Факт получен:", fact)

# Отправляем в Telegram
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
data = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": fact,
    "parse_mode": "Markdown",
}
response = requests.post(url, data=data)
print("✅ Telegram ответ:", response.status_code, response.text)
