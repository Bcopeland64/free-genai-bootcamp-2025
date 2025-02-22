# chat.py
import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration
from typing import Optional, Dict, Any

# Correct model ID for AraT5
MODEL_ID = "UBC-NLP/AraT5-base"

class ArabicChat:
    def __init__(self, model_id: str = MODEL_ID):
        """
        Initialize Arabic chat client with AraT5 model.
        
        Args:
            model_id (str): Hugging Face model ID for AraT5.
        """
        self.tokenizer = T5Tokenizer.from_pretrained(model_id)
        self.model = T5ForConditionalGeneration.from_pretrained(model_id)

    def generate_response(self, message: str, inference_config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Generate a response using the AraT5 model.
        
        Args:
            message (str): User input message.
            inference_config (Optional[Dict[str, Any]]): Configuration for text generation.
        
        Returns:
            Optional[str]: Generated response or None if an error occurs.
        """
        if inference_config is None:
            inference_config = {
                "max_length": 50,  # Maximum length of the generated response
                "temperature": 0.7,  # Controls randomness (lower = more deterministic)
                "num_beams": 5,  # Beam search for better quality
                "early_stopping": True,  # Stop generation early if appropriate
            }

        try:
            # Encode the input message
            input_ids = self.tokenizer.encode(message, return_tensors="pt")
            
            # Generate response
            outputs = self.model.generate(input_ids, **inference_config)
            
            # Decode and return the response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return None


if __name__ == "__main__":
    # Test the ArabicChat class
    chat = ArabicChat()
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        response = chat.generate_response(user_input)
        print("Bot:", response)