import google.generativeai as genai
from instance import config

class GeminiClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)

    def generate_content(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API Error: {str(e)}")
