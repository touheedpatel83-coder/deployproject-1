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

def create_prompt(topic, audience, output_format):
    return f"""
    Act as an experienced technical educator.

    Topic: {topic}
    Target audience: {audience}
    Output format: {output_format}

    Instructions:
    1. Explain the concept accurately.
    2. Include one practical example.
    3. Use language appropriate for the audience.
    4. End with one practice question.
    """
def generate_lesson(topic, audience, output_format):
    prompt = create_prompt(topic, audience, output_format)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    print("\nGENERATED LESSON\n")
    print(response.text)


if __name__ == "__main__":
    generate_lesson(
        topic="Ai Agents",
        audience="Working Professions",
        output_format="bullet points"
    )



