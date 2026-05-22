import os
from openai import OpenAI, AuthenticationError
from dotenv import load_dotenv

# Shared OpenAI client for all assignments.
# Centralised here so both assignments (my_ai_assistant, business_assistant)
# import from one place. If we ever want to swap OpenAI for another provider
# (e.g. Anthropic, Gemini, a local Ollama model), we only need to change this
# file — every assignment that imports `client` will automatically use the
# new provider without any other code changes needed.

load_dotenv()

try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file.")

    client = OpenAI(api_key=api_key)
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    print("✅ API key loaded successfully!")
    print(f"Key starts with: {api_key[:8]}...")

except ValueError as e:
    print(f"❌ Configuration error: {e}")
    raise
except AuthenticationError as e:
    print("❌ OpenAI rejected the API key. Verify it at platform.openai.com.")
    raise
except Exception as e:
    print(f"❌ Unexpected error during setup: {e}")
    raise
