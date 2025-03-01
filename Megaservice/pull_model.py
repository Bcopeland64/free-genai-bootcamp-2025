#!/usr/bin/env python3
"""
Simple script to pull a model from Ollama.
"""

from apps.ollama_utils import pull_model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model to pull
MODEL_NAME = "llama3.2:1b"  # Change this to your desired model

def main():
    print(f"Pulling model: {MODEL_NAME}")
    success, message = pull_model(MODEL_NAME)
    if success:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")

if __name__ == "__main__":
    main()