import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("No API key")
    exit(1)

client = genai.Client(api_key=api_key)

for model in client.models.list():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)
