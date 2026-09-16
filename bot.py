import os
import time
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

message = """🤖 QA Telegram Bot

Hello! 👋

This is an automated message from my cloud-hosted QA bot.

🧪 Manual Testing
🔌 API Testing
🤖 Test Automation

More QA content will be coming soon! 🚀
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.json())


