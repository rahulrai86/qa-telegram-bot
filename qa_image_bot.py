import os
import random
import requests


PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

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


if not PEXELS_API_KEY:
    raise Exception("PEXELS_API_KEY is not configured.")


print("Starting QA image search...")


# Select a QA topic
topic = random.choice(QA_TOPICS)

print(f"Selected QA topic: {topic}")


# Search Pexels
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


# Select a random image
photo = random.choice(photos)

photo_url = photo["url"]
photographer = photo["photographer"]
image_url = photo["src"]["large"]


print(f"Selected image: {photo_url}")
print(f"Photographer: {photographer}")
print(f"Image URL: {image_url}")


# Download image
print("Downloading image...")


image_response = requests.get(
    image_url,
    timeout=30
)

image_response.raise_for_status()


with open(IMAGE_FILE, "wb") as file:
    file.write(image_response.content)


print("Image downloaded successfully.")
print(f"Saved image as: {IMAGE_FILE}")
print(f"Topic: {topic}")
print(f"Photographer: {photographer}")
print(f"Pexels photo: {photo_url}")
print("QA image search completed successfully.")
