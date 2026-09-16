import os
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY is not configured.")


client = OpenAI(
    api_key=OPENAI_API_KEY
)


prompt = """
Create a professional realistic editorial-style image about software quality assurance.

Scene:
A modern software testing team working in a technology office.
A QA engineer is investigating a software defect using multiple monitors.
The screens show realistic but generic software testing dashboards, test cases,
logs, and application screens.

Style:
Photorealistic, professional technology photography,
modern enterprise software environment,
cinematic but natural lighting,
high quality,
clean composition,
realistic people and computers.

Important:
Do not create an infographic.
Do not create a presentation slide.
Do not use large text.
Do not include captions.
Do not include logos.
Do not include watermarks.
The image should look like a professional technology article photograph.
"""


print("Starting QA image generation...")

result = client.images.generate(
    model="gpt-image-2",
    prompt=prompt,
    size="1536x1024"
)

print("Image generated successfully.")

print(result)
