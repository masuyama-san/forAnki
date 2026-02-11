import google.generativeai as genai
import os
import sys

# Try to find .env file
env_path = os.path.join(os.path.dirname(__file__), "instance", ".env")
if not os.path.exists(env_path):
    env_path = os.path.join(os.path.dirname(__file__), ".env")

# Manually load .env since python-dotenv might not be installed or working as expected in this context
api_key = None
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    api_key = parts[1].strip().strip('"').strip("'")
                    break

print(f"Loaded API Key (masked): {api_key[:5]}... if exists")

if not api_key:
    # try environment variable
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    sys.exit(1)

genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
