import requests

url = "https://feeds.feedburner.com/softwaretestinghelp"

response = requests.get(url, timeout=20)

print("Status:", response.status_code)
print("Content length:", len(response.text))
print(response.text[:500])
