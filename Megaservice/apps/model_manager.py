import os
from .ollama_utils import get_available_models, pull_model

class ModelManager:
    """Class for managing Ollama models."""
    
    def get_models(self):
        """Get a list of available models."""
        return get_available_models()
    
    def download_model(self, model_name):
        """Download a model from Ollama."""
        success, message = pull_model(model_name)
        if success:
            return True, f"Successfully downloaded model: {model_name}"
        else:
            return False, f"Failed to download model: {message}"