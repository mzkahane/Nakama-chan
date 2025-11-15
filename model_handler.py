import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig
)
import logging
import asyncio

logger = logging.getLogger(__name__)

class OpenHermesModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.model_name = "teknium/OpenHermes-2.5-Mistral-7B"

    async def load_model(self):
        # Load model with 4-bit quantization
        try:
            print(f"Loading model: {self.model_name}")

            # 4-bit quantization config
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True, 
                bnb_4bit_quant_type="nf4", 
                bnb_4bit_compute_dtype=torch.float16, 
                bnb_4bit_use_double_quant=True
            )

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                trust_remote_code=True, 
                use_fast=False
            )

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load model with quantization
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name, 
                quantization_config=bnb_config, 
                device_map="auto", 
                trust_remote_code=True
            )

            self.is_loaded = True
            print("Model loaded successfully!")

        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def generate_response(self, prompt: str) -> str:
        # Generate response using the model
        if not self.is_loaded:
            return "Model still loading..."
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, 
                    max_new_tokens=150, 
                    temperature=0.7, 
                    do_sample=True, 
                    system_prompt="You are Nakama, a helpful and friendly AI assistant. You are witty, kind, and enjoy helping users with their questions. Keep responses natural and conversational. Avoid overly formal language and be engaging."
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the new text
            response = response.replace(prompt, "").strip()

            return response or "I couldn't generate a response."
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
model_handler = OpenHermesModel()