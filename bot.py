import os
import random
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

topics = [
    {
        "title": "Boundary Value Analysis",
        "explanation": "Boundary Value Analysis is a test case design technique where we test values at the edges of an input range. For example, if the valid age is 18 to 60, test 17, 18, 19, 59, 60 and 61."
    },
    {
        "title": "Equivalence Partitioning",
        "explanation": "Equivalence Partitioning divides input data into groups that are expected to behave similarly. Instead of testing every value, we select representative values from each valid and invalid group."
    },
    {
        "title": "Regression Testing",
        "explanation": "Regression Testing verifies that recent code changes have not broken existing functionality. It is commonly performed after bug fixes, enhancements or new feature development."
    },
    {
        "title": "Smoke Testing",
        "explanation": "Smoke Testing is a quick check of the major functions of an application to determine whether the build is stable enough for detailed testing."
    },
    {
        "title": "Sanity Testing",
        "explanation": "Sanity Testing is focused testing performed after a small change or bug fix to verify that the specific functionality works correctly and that the change has not introduced obvious issues."
    },
    {
        "title": "Exploratory Testing",
        "explanation": "Exploratory Testing combines learning, test design and execution at the same time. Testers explore the application without relying entirely on predefined test cases."
    },
    {
        "title": "Negative Testing",
        "explanation": "Negative Testing verifies how an application behaves when it receives invalid, unexpected or incorrect input. The goal is to make sure the application handles invalid situations properly."
    },
    {
        "title": "API Testing",
        "explanation": "API Testing validates application programming interfaces directly by checking requests, responses, status codes, headers, authentication and data."
    }
]

topic = random.choice(topics)

message = f"""🧪 QA Testing Topic

📌 {topic["title"]}

💡 Explanation:
{topic["explanation"]}

🤖 Automation By Rahul
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
