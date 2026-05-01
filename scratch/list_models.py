import os
from google import genai
from app.core.config import settings

def list_models():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    try:
        print("Listing available models...")
        for model in client.models.list():
            print(f"Model Name: {model.name}")
            print(f"Supported Methods: {model.supported_generate_methods}")
            print("-" * 20)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
