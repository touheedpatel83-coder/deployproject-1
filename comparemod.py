import os
import time
import csv
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Add GEMINI_API_KEY to your .env file.")

client = genai.Client(api_key=api_key)

# Keep this prompt identical for every model
prompt = """
You are a Python instructor teaching engineering students.

Explain exception handling in Python.
Include:
1. A simple definition
2. A practical real-world example
3. A short summary

Use beginner-friendly language and stay within 250 words.
"""

models = [
    "gemini-3.5-flash-lite",
    "gemini-nano-banana-2.1",
    "gemini-3.1-flash-lite",
]

results = []

for model in models:
    print(f"\nTesting model: {model}")

    try:
        start_time = time.perf_counter()

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=400
            )
        )

        elapsed = time.perf_counter() - start_time
        usage = response.usage_metadata

        input_tokens = (
            getattr(usage, "prompt_token_count", None)
            if usage else None
        )
        output_tokens = (
            getattr(usage, "candidates_token_count", None)
            if usage else None
        )
        total_tokens = (
            getattr(usage, "total_token_count", None)
            if usage else None
        )

        answer = response.text or ""

        print(f"Latency: {elapsed:.2f} seconds")
        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Total tokens: {total_tokens}")
        print("\nResponse:\n", answer)

        results.append({
            "model": model,
            "latency_seconds": round(elapsed, 3),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "response": answer,
            "error": ""
        })

    except Exception as error:
        print(f"Error with {model}: {error}")

        results.append({
            "model": model,
            "latency_seconds": None,
            "input_tokens": None,
            "output_tokens": None,
            "total_tokens": None,
            "response": "",
            "error": str(error)
        })

# Save results for analysis
filename = "gemini_comparison.csv"

with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=results[0].keys()
    )
    writer.writeheader()
    writer.writerows(results)

print(f"\nComparison saved to {filename}")
print("Review the CSV and evaluate answer quality.")