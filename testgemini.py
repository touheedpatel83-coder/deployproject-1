import os
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

# Read API key securely
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send a prompt to Gemini
response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Hello Gemini"
)

# Display response
print("\nGemini Response:\n")
print(response.text)