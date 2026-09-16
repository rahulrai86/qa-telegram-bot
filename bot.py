import os
import random
import requests
import xml.etree.ElementTree as ET
import re
import json
from html import unescape

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_URL = "https://feeds.feedburner.com/softwaretestinghelp"
HISTORY_FILE = "posted_articles.json"


def clean_html(text):
    """Remove HTML tags and clean RSS description text."""
    text = unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_posted_articles():
    """Load the list of already posted articles."""

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("posted", [])


def save_posted_articles(posted_articles):
    """Save posted article links to the history file."""

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"posted": posted_articles},
            file,
            indent=2
        )


def get_qa_articles():
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

    return articles


def select_article(articles, posted_articles):
    """Select an article that has not been posted yet."""

    available_articles = []

    for article in articles:
        title = article.findtext(
            "title",
            default="QA Testing Article"
        )

        link = article.findtext(
            "link",
            default=""
        )

        if link and link not in posted_articles:
            available_articles.append(
                {
                    "title": title,
                    "link": link,
                    "description": article.findtext(
                        "description",
                        default=""
                    )
                }
            )

    # If all articles have already been posted,
    # start a new cycle.
    if not available_articles:
        print("All articles have been posted.")
        print("Starting a new article cycle.")

        posted_articles.clear()

        for article in articles:
            title = article.findtext(
                "title",
                default="QA Testing Article"
            )

            link = article.findtext(
                "link",
                default=""
            )

            if link:
                available_articles.append(
                    {
                        "title": title,
                        "link": link,
                        "description": article.findtext(
                            "description",
                            default=""
                        )
                    }
                )

    if not available_articles:
        raise Exception("No available articles found.")

    return random.choice(available_articles)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

print("Starting QA Telegram Bot...")

posted_articles = load_posted_articles()

print(
    f"Previously posted articles: "
    f"{len(posted_articles)}"
)

articles = get_qa_articles()

print(
    f"Articles available in RSS feed: "
    f"{len(articles)}"
)

article = select_article(
    articles,
    posted_articles
)

title = article["title"]
link = article["link"]
description = clean_html(article["description"])

print(f"Selected article: {title}")
print(f"Link: {link}")


message = f"""🧪 QA Testing Topic

📌 {title}

💡 About this topic:
{description[:1000]}

🔗 Read more:
{link}

🤖 Automation By Rahul
"""


# --------------------------------------------------
# SEND MESSAGE TO TELEGRAM
# --------------------------------------------------

telegram_url = (
    f"https://api.telegram.org/bot"
    f"{BOT_TOKEN}/sendMessage"
)

response = requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=20
)

response.raise_for_status()

print("Telegram message sent successfully!")


# --------------------------------------------------
# SAVE ARTICLE AS POSTED
# --------------------------------------------------

posted_articles.append(link)

save_posted_articles(posted_articles)

print(
    f"Article history updated. "
    f"Total posted: {len(posted_articles)}"
)

print("QA Telegram Bot completed successfully.")
