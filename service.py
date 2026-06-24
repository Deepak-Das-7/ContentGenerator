# services.py
import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: str, model_name: str = 'gemini-2.5-flash'):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)

    def generate_study_material(self, compiled_prompt: str) -> str:
        """Sends prompt to LLM and returns the raw string response."""
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(compiled_prompt)
        return response.text