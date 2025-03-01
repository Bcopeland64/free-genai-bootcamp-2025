import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:8008/api")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemma:2b")

def get_available_models():
    """Get list of available models from Ollama."""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        if response.status_code == 200:
            return response.json()["models"]
        else:
            return []
    except Exception as e:
        print(f"Error getting models: {e}")
        return []

def pull_model(model_name):
    """Pull (download) a model from Ollama."""
    try:
        payload = {"model": model_name}
        response = requests.post(f"{OLLAMA_API_URL}/pull", json=payload, stream=True)
        
        if response.status_code == 200:
            return True, "Model pulled successfully"
        else:
            return False, f"Failed to pull model: {response.text}"
    except Exception as e:
        return False, f"Error pulling model: {e}"

def generate_text(model_name, prompt, temperature=0.7, max_tokens=2000):
    """Generate text using Ollama API."""
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_API_URL}/generate", json=payload)
        
        if response.status_code == 200:
            try:
                return True, response.json().get("response", "No response generated")
            except json.JSONDecodeError as e:
                return False, f"Failed to parse JSON response: {e}"
        else:
            return False, f"Failed to generate text: {response.text}"
    except Exception as e:
        return False, f"Error generating text: {e}"

def check_ollama_connection():
    """Check if Ollama API is accessible."""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        return response.status_code == 200
    except:
        return False