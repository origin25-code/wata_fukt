import os
import requests
import openai

# Проверка ключей
print("🔑 OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY")[:5], "...")
print("🔑 TELEGRAM_BOT_TOKEN:", os.environ.get("TELEGRAM_BOT_TOKEN")[:5], "...")
print("🔑 CHAT_ID:", os.environ.get("DEBUG_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID"))

# Промпт
with open("fact_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

try:
    # Генерация факта
    print("🚀 Запрос к OpenAI...")
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Сгенерируй 1 факт"},
        ],
        temperature=1.0,
        request_timeout=30,
    )
    fact = response.choices[0].message.content.strip()
    print("✅ Факт получен:", fact)

except openai.error.OpenAIError as e:
    fact = f"❌ OpenAI error: {e}"
    print(fact)

# Telegram
token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("DEBUG_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID")

try:
    print("📬 Отправляем в Telegram...")
    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": fact}
    )
    print("📦 Telegram ответ:", resp.status_code, resp.text)

except Exception as e:
    print("❌ Ошибка Telegram:", e)
