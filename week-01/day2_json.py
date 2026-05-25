# week-01/day2_json.py
# Topic: JSON Handling for AI Development
# Why: Every AI API response is JSON. You'll parse these hundreds of times

import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================
# PART 1: JSON basics — converting between dict and JSON string
# ============================================================

# A Python dictionary — this is what you work with in code

profile = {
    "name": "Anshul",
    "role": "Senior System Engineer",
    "company": "TCS",
    "location": "Germany",
    "skills": ["SAS", "Python", "Power BI"],
    "experience_years": 7,
    "is_learning_genai": True
}

# dict -> JSON string
# use this when : saving to file, sending over network , logging
json_string = json.dumps(profile, indent=2)

print("==== dict -> JSON string ====")
print(json_string)
print(f"Type:{type(json_string)}")

# JSON string -> dict
# Use when : receiving API response, reading from file

parsed_back = json.loads(json_string)
print("\n==== JSON string -> dict ====")
print(f"Name  : {parsed_back['name']}")
print(f"Skills  : {parsed_back['skills']}")
print(f"Skills_1  : {parsed_back['skills'][0]}")
print(f"Type  : {type(parsed_back)}")

# ============================================================
# PART 2: Save and load JSON from files
# Use this for: caching API responses, logging, storing results
# ============================================================

# __file__ = full path of this script
# os.path.dirname + abspath = folder containing this script
# This works regardless of which directory you run from

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(SCRIPT_DIR, "profile.json")

# Save to file 
with open(profile_path, "w") as f:
    json.dump(profile, f, indent=2)
    # json.dump -> writes directly to the file
    # json.dumps -> returns a string

print(f"\n Saved to : {profile_path}")

# Load the file 

with open (profile_path, "r") as f:
    loaded = json.load(f)
    # json.load -> reads from file
    # json.loads -> reads from string

print(f"Loaded name : {loaded['name']}")
print(f"Loaded location : {loaded['location']}")
print(f"Loaded Company : {loaded['company']}")


# ============================================================
# PART 3: Make Claude return structured JSON
# THIS IS THE MOST IMPORTANT PART — used in every real AI project
# ============================================================

# The key technique: tell Claude EXACTLY what JSON to return
# and say "no explanation, no markdown, raw JSON only"

text_to_analyze = """
Anshul Raghuvanshi is a Senior Systems Engineer at TCS with 7 years 
of experience. He is currently based in Frankfurt, Germany on an 
intra-company transfer. He specializes in SAS 9.4 on IBM Mainframe 
z/OS and is actively learning Python and Generative AI to transition 
into an AI Engineer role targeting 20-35 LPA.
"""

prompt = f"""Extract information from the text below.
Return ONLY a valid JSON object.
No explanation. No markdown. No backticks. Raw JSON only.

Text:{text_to_analyze}

Return exactly this JSON structure:
{{
    "full_name": "string",
    "current_role": "string",
    "company": "string",
    "experience_years": number,
    "current_location": "string",
    "technical_skills": ["list", "of", "skills"],
    "learning_goals": ["list", "of", "goals"],
    "target_salary_lpa": "string"
}}"""

print(f"\n==== Asking Claude to return structured JSON === ")

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens = 400,
    messages=[
        {
            "role" : "user",
            "content":prompt
        }
    ]
)

raw_text = response.content[0].text
print(f"Raw Claude response:\n{raw_text}")



# ============================================================
# PART 4: Safely parse Claude's JSON response
# CRITICAL: Claude adds markdown backticks ~20% of the time
# even when told not to. This cleaner handles that.
# ============================================================

print("\n==== Parsing Claude's Response ====")

# Step 1 - Clean the raw response before parsing 
# strip() removes leading/trailing whitespace and newlines

cleaned = raw_text.strip()

# Remove opening fence if present (```json or```)
# startswith checks if string begins with these characters

if cleaned.startswith("```"):
    cleaned = cleaned.split("\n",1)[1]

if cleaned.endswith("```"):
    cleaned = cleaned.rsplit("\n",1)[0]

# Final whitespace cleanup
cleaned = cleaned.strip()

print(f"Cleaned response:\n{cleaned}")

try:
    extracted = json.loads(cleaned)
    print("\n==== Parsed Successfully ===")
    print(f"Name     : {extracted['full_name']}")
    print(f"Role     : {extracted['current_role']}")
    print(f"Company  : {extracted['company']}")
    print(f"Location : {extracted['current_location']}")
    print(f"Skills   : {', '.join(extracted['technical_skills'])}")
    print(f"Goals    : {', '.join(extracted['learning_goals'])}")
    print(f"Target   : {extracted['target_salary_lpa']} lpa")

except json.JSONDecodeError as e:
    # This catches cases where claude added estra text around the JSON
    print(f"JSON parsing failed: {e}")
    print(f"Raw respionse was: {cleaned}")