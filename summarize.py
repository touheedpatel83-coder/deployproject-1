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

article=""" Area commands were the major operational and administrative formations of the Royal Australian Air Force (RAAF) between 1940 and 1954. Established in response to the outbreak of World War II, they underpinned the Air Force's geographically based command-and-control system for the duration of the conflict and into the early years of the Cold War, until being superseded by a functional control system made up of Home, Training, and Maintenance Commands.
The area commands and their responsibilities evolved over time according to changing circumstances. The RAAF established four commands to begin with in 1940–41: Southern Area, Central Area, Western Area, and Northern Area. The commands oversaw most of the operations, training, and maintenance within their boundaries. A concession to functional control occurred in mid-1941, when the Air Force formed two groups that assumed the training role of the southern and eastern 
states; Central Area was disbanded and most of its units taken over by Northern and Southern Areas, and the newly formed No. 2 (Training) Group. The area structure was further revised in 1942, following the outbreak of the Pacific War; Northern Area was split into North-Eastern Area and North-Western Area, and a new command, Eastern Area, was created, making a total of five commands. The same year, the RAAF formed two functional groups that assumed the maintenance role 
of the area commands; the latter focused on operations until the end of hostilities. A new area command covering RAAF units in New Guinea, Northern Command, was formed in 1944 and dissolved soon after the war.
"""

prompt=f"""
summarize below article in 100 words
{article}
"""

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
)
print("\nGemini Response:\n")
print(response.text)