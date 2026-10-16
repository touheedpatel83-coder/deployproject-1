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


from pypdf import PdfReader

def read_resume_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    if not text.strip():
        raise ValueError("No readable text found in the PDF.")

    return text


resume_text = read_resume_pdf("sample_resume.pdf  ")

#print(resume_text)

from pydantic import BaseModel, Field, model_validator


class ResumeAnalysis(BaseModel):
    student_name: str = "Not Available"
    email: str = "Not Available"
    phone: str = "Not Available"
    qualification: str = "Not Available"
    college: str = "Not Available"

    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

    experience: str = "Not Available"
    career_objective: str = "Not Available"

    @model_validator(mode="before")
    @classmethod
    def fill_missing_values(cls, data):
        if not isinstance(data, dict):
            return data

        data = data.copy()

        text_fields = [
            "student_name", "email", "phone",
            "qualification", "college",
            "experience", "career_objective"
        ]

        list_fields = [
            "skills", "projects", "certifications"
        ]

        for field in text_fields:
            value = data.get(field)

            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                data[field] = "Not Available"

        for field in list_fields:
            if data.get(field) is None:
                data[field] = []

        return data



response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=f"""
    You are a resume information extraction assistant.

    Extract these fields from the resume:
    student_name, email, phone, qualification, college,
    skills, projects, certifications, experience,
    career_objective.

    Rules:
    1. Extract only details supported by the resume.
    2. Do not invent missing information.
    3. Use "Not Available" for missing text fields.
    4. Use empty lists for missing list fields.

    Resume text:
    {resume_text}
    """,
    config={
        "response_mime_type": "application/json",
        "response_schema": ResumeAnalysis
    }
)

print(response.text)


from pydantic import ValidationError

try:
    resume = ResumeAnalysis.model_validate_json(response.text)

    print("Validation successful!")
    print(resume.model_dump_json(indent=2))

except ValidationError as error:
    print("Validation failed!")
    print(error)