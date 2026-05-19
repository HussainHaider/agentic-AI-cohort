from openai import OpenAI
import os
from dotenv import load_dotenv

# Shared OpenAI client for all assignments.
# Centralised here so both assignments (my_ai_assistant, business_assistant)
# import from one place. If we ever want to swap OpenAI for another provider
# (e.g. Anthropic, Gemini, a local Ollama model), we only need to change this
# file — every assignment that imports `client` will automatically use the
# new provider without any other code changes needed.

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if client.api_key:
    print("✅ API key loaded successfully!")
    print(f"Key starts with: {client.api_key[:8]}...")
else:
    print("❌ API key not found! Check your .env file.")
