import os
import random
import requests
import json


PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

IMAGE_FILE = "qa_image.jpg"
HISTORY_FILE = "posted_images.json"


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
# LOAD POSTED IMAGE HISTORY
# --------------------------------------------------

def load_posted_images():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data.get("posted", [])


# --------------------------------------------------
# SAVE POSTED IMAGE HISTORY
# --------------------------------------------------

def save_posted_images(posted_images):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "posted": posted_images
            },
            file,
            indent=2
        )


# --------------------------------------------------
# VALIDATE ENVIRONMENT VARIABLES
# --------------------------------------------------

if not PEXELS_API_KEY:
    raise Exception(
        "PEXELS_API_KEY is not configured."
    )

if not BOT_TOKEN:
    raise Exception(
        "TELEGRAM_BOT_TOKEN is not configured."
    )

if not CHAT_ID:
    raise Exception(
        "TELEGRAM_CHAT_ID is not configured."
    )


print("Starting QA image bot...")


# --------------------------------------------------
# LOAD HISTORY
# --------------------------------------------------

posted_images = load_posted_images()

print(
    f"Previously posted images: "
    f"{len(posted_images)}"
)


# --------------------------------------------------
# SELECT QA TOPIC
# --------------------------------------------------

topic = random.choice(QA_TOPICS)

print(
    f"Selected QA topic: {topic}"
)


# --------------------------------------------------
# SEARCH PEXELS
# --------------------------------------------------

pexels_url = (
    "https://api.pexels.com/v1/search"
)

headers = {
    "Authorization": PEXELS_API_KEY
}

params = {
    "query": topic,
    "orientation": "landscape",
    "per_page": 20
}


response = requests.get(
    pexels_url,
    headers=headers,
    params=params,
    timeout=20
)

response.raise_for_status()

data = response.json()

photos = data.get(
    "photos",
    []
)


if not photos:

    raise Exception(
        f"No images found for topic: {topic}"
    )


# --------------------------------------------------
# FIND UNUSED IMAGE
# --------------------------------------------------

available_photos = []

for photo in photos:

    photo_id = str(
        photo["id"]
    )

    if photo_id not in posted_images:

        available_photos.append(photo)


# --------------------------------------------------
# IF ALL IMAGES WERE USED
# --------------------------------------------------

if not available_photos:

    print(
        "All images from this search "
        "have already been posted."
    )

    print(
        "Starting a new image cycle."
    )

    posted_images.clear()

    available_photos = photos


# --------------------------------------------------
# SELECT IMAGE
# --------------------------------------------------

photo = random.choice(
    available_photos
)

photo_id = str(
    photo["id"]
)

photo_url = photo["url"]

photographer = photo["photographer"]

image_url = photo["src"]["large"]


print(
    f"Selected image ID: {photo_id}"
)

print(
    f"Photographer: {photographer}"
)

print(
    f"Photo page: {photo_url}"
)


# --------------------------------------------------
# DOWNLOAD IMAGE
# --------------------------------------------------

print(
    "Downloading image..."
)


image_response = requests.get(
    image_url,
    timeout=30
)

image_response.raise_for_status()


with open(
    IMAGE_FILE,
    "wb"
) as file:

    file.write(
        image_response.content
    )


print(
    "Image downloaded successfully."
)


# --------------------------------------------------
# SEND IMAGE TO TELEGRAM
# --------------------------------------------------

print(
    "Sending image to Telegram..."
)


telegram_url = (
    f"https://api.telegram.org/bot"
    f"{BOT_TOKEN}/sendPhoto"
)


caption = f"""🧪 QA Testing

📌 Topic: {topic.title()}

Professional QA/testing visual.

🤖 Automation By Rahul
"""


with open(
    IMAGE_FILE,
    "rb"
) as image:

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


print(
    "Image sent successfully to Telegram."
)


# --------------------------------------------------
# SAVE IMAGE HISTORY
# --------------------------------------------------

posted_images.append(
    photo_id
)

save_posted_images(
    posted_images
)


print(
    f"Image history updated. "
    f"Total posted: {len(posted_images)}"
)


print(
    "QA image bot completed successfully."
)
