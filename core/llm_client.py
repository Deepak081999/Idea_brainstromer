import google.generativeai as genai
import os


# Configure Gemini API Key
os.environ["GOOGLE_API_KEY"] = "GEMINI_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


class GeminiLLM:
    def __init__(self, model_name="gemini-2.0-flash-001"):
        self.model = genai.GenerativeModel(model_name)


    def ask(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
