import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("No API key")
    exit(1)

try:
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Hello, say something short.',
    )
    print("Success: ", response.text)
except Exception as e:
    print("Error:", type(e).__name__, e)

