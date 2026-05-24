# Step 1: Import libraries
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Step 2: Load .env file so Python can read ANTHROPIC_API_KEY
load_dotenv()

# 3 : Creata ANthropic Client
# Same concept as OpenAI client - obe object to handle API calls

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

#4: Make your first API call
# message.create() is Anthropic's equivalent of OpenAI's chat.completeions.create

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens = 100,
    messages = [
        {
            "role":"user",
            "content":"Hello! I just made my first ever LLM API call.Say congratulations in 1 sentence."
        }
    ]
)

#5 : Extract the response text
# Anthropic's response structure is slightly different from OpenAI's
# The text lives in response.content[0].text

answer = response.content[0].text
print(f"Claude says: {answer}")

#6 : check token usage
print(f"\nTokens used:")
print(f" Input tokens: {response.usage.input_tokens}")
print(f" Output tokens: {response.usage.output_tokens}")

