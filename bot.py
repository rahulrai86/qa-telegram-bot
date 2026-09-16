import os
import random
import requests
import xml.etree.ElementTree as ET
import re
from html import unescape

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_URL = "https://feeds.feedburner.com/softwaretestinghelp"


def clean_html(text):
    """Remove HTML tags and clean RSS description text."""
    text = unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_qa_article():
    """Fetch QA/testing articles from the RSS feed."""

    response = requests.get(RSS_URL, timeout=20)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    channel = root.find("channel")

    if channel is None:
        raise Exception("RSS channel not found")

    articles = channel.findall("item")

    if not articles:
        raise Exception("No articles found in RSS feed")

    article = random.choice(articles)

    title = article.findtext("title", default="QA Testing Article")
    link = article.findtext("link", default="")
    description = article.findtext("description", default="")

    description = clean_html(description)

    return title, link, description


title, link, description = get_qa_article()

message = f"""🧪 QA Testing Topic

📌 {title}

💡 About this topic:
{description[:1000]}

🔗 Read more:
{link}

🤖 Automation By Rahul
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=20
)

response.raise_for_status()

print("Telegram message sent successfully!")
print(response.json())
