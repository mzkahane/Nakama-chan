from google import genai
from google.genai import types
import os

import config

class GeminiModel:
    def __init__(self):
        self.client = None
        self.is_loaded = False
        self.model = config.MODEL_NAME
        
    async def load_model(self):
        KEY = os.getenv('GEMINI_API_KEY')
        if not KEY:
            print("ERROR: GEMINI_API_KEY not found in .env")
            exit(1)
        self.client = genai.Client(api_key=KEY)
        self.is_loaded = True
    
    async def generate_response(self, user_input: str) -> str:
        if not self.is_loaded:
            return "Model still loading..."
        try:
            response = await self.client.aio.models.generate_content(
                model = self.model, 
                contents = user_input, 
                config = types.GenerateContentConfig(
                    system_instruction=config.SYSTEM_PROMPT, 
                    max_output_tokens=config.MAX_TOKENS
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
model_handler = GeminiModel()
