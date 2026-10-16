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
import streamlit as st
st.title("LLM Prompt and Response App")


# Get user prompt
prompt = st.text_area("Enter your prompt:")

# Generate response
if st.button("Generate Response"):

    if prompt.strip():

        with st.spinner("LLM is generating response..."):

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

        st.subheader("LLM Response")
        st.write(response.text)

    else:
        st.warning("Please enter a prompt.")