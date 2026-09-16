import requests
import xml.etree.ElementTree as ET

RSS_URL = "https://feeds.feedburner.com/softwaretestinghelp"

response = requests.get(RSS_URL, timeout=20)
response.raise_for_status()

root = ET.fromstring(response.content)

channel = root.find("channel")

if channel is None:
    raise Exception("RSS channel not found")

items = channel.findall("item")

print(f"Found {len(items)} articles")

for item in items[:5]:
    title = item.findtext("title", default="No title")
    link = item.findtext("link", default="No link")
    description = item.findtext("description", default="No description")

    print("\n------------------------------")
    print("TITLE:", title)
    print("LINK:", link)
    print("DESCRIPTION:", description[:300])
