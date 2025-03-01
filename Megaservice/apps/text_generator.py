import os
from .ollama_utils import generate_text, DEFAULT_MODEL

class TextGenerator:
    """Class for generating text using Ollama LLM models."""
    
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
    
    def generate(self, prompt, temperature=0.7, max_tokens=2000):
        """Generate text based on the prompt."""
        success, response = generate_text(
            self.model_name, 
            prompt, 
            temperature, 
            max_tokens
        )
        
        if success:
            return response
        else:
            raise Exception(f"Text generation failed: {response}")
    
    def set_model(self, model_name):
        """Change the model used for generation."""
        self.model_name = model_name
        return f"Model changed to {model_name}"