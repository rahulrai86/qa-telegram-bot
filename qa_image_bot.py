import os
import random
import requests


PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

IMAGE_FILE = "qa_image.jpg"


QA_TOPICS = [
    "software testing",
    "software tester",
    "quality assurance",
    "test automation",
    "API testing",
    "bug testing",
    "software developer testing",
    "computer programming testing",
    "CI CD software",
    "web application testing"
]


# --------------------------------------------------
# VALIDATE ENVIRONMENT VARIABLES
# --------------------------------------------------

if not PEXELS_API_KEY:
    raise Exception("PEXELS_API_KEY is not configured.")

if not BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN is not configured.")

if not CHAT_ID:
    raise Exception("TELEGRAM_CHAT_ID is not configured.")


print("Starting QA image bot...")


# --------------------------------------------------
# SELECT QA TOPIC
# --------------------------------------------------

topic = random.choice(QA_TOPICS)

print(f"Selected QA topic: {topic}")


# --------------------------------------------------
# SEARCH PEXELS
# --------------------------------------------------

pexels_url = "https://api.pexels.com/v1/search"

headers = {
    "Authorization": PEXELS_API_KEY
}

params = {
    "query": topic,
    "orientation": "landscape",
    "per_page": 10
}


response = requests.get(
    pexels_url,
    headers=headers,
    params=params,
    timeout=20
)

response.raise_for_status()

data = response.json()

photos = data.get("photos", [])


if not photos:
    raise Exception(
        f"No images found for topic: {topic}"
    )


# --------------------------------------------------
# SELECT IMAGE
# --------------------------------------------------

photo = random.choice(photos)

photo_url = photo["url"]
photographer = photo["photographer"]
image_url = photo["src"]["large"]


print(f"Selected image: {photo_url}")
print(f"Photographer: {photographer}")


# --------------------------------------------------
# DOWNLOAD IMAGE
# --------------------------------------------------

print("Downloading image...")


image_response = requests.get(
    image_url,
    timeout=30
)

image_response.raise_for_status()


with open(IMAGE_FILE, "wb") as file:
    file.write(image_response.content)


print("Image downloaded successfully.")


# --------------------------------------------------
# SEND IMAGE TO TELEGRAM
# --------------------------------------------------

print("Sending image to Telegram...")


telegram_url = (
    f"https://api.telegram.org/bot"
    f"{BOT_TOKEN}/sendPhoto"
)


caption = f"""🧪 QA Testing

📌 Topic: {topic.title()}

Professional QA/testing visual.

📸 Photo by {photographer}
🔗 Pexels: {photo_url}

🤖 Automation By Rahul
"""


with open(IMAGE_FILE, "rb") as image:

    telegram_response = requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "caption": caption
        },
        files={
            "photo": image
        },
        timeout=30
    )


telegram_response.raise_for_status()


print("Image sent successfully to Telegram.")

print("QA image bot completed successfully.")
