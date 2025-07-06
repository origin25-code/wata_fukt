import os
import requests
import openai

# Логируем первые символы ключей
print("🧪 KEY:", os.environ.get("OPENAI_API_KEY")[:5], "...")
print("🧪 TG_TOKEN:", os.environ.get("TELEGRAM_BOT_TOKEN")[:5], "...")

# Промпт
with open("fact_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

openai.api_key = os.environ["OPENAI_API_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Сгенерируй 1 факт"},
    ],
    temperature=1,
)

fact = response.choices[0].message.content.strip()
print("📦 Generated Fact:\n", fact)

# Отправка в Telegram
tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ.get("DEBUG_CHAT_ID", os.environ["TELEGRAM_CHAT_ID"])

resp = requests.post(
    f"https://api.telegram.org/bot{tg_token}/sendMessage",
    data={"chat_id": chat_id, "text": fact},
)

print("📬 Telegram Response:", resp.status_code, resp.text)
