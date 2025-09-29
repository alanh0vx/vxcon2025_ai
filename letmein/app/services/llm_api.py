import requests
import json
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaAPI:
    def __init__(self, base_url: str = "http://host.docker.internal:11434"):
        """
        Initialize Ollama API client
        
        Args:
            base_url: Ollama server URL (using Docker internal networking to host)
        """
        self.base_url = base_url
        self.model_name = "gemma3:270m"
        
    def _make_request(self, endpoint: str, data: dict) -> dict:
        """
        Make HTTP request to Ollama API
        
        Args:
            endpoint: API endpoint
            data: Request payload
            
        Returns:
            Response data
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, json=data, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Ollama: {e}")
            raise
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: User input prompt
            system_prompt: System/context prompt
            
        Returns:
            Generated response text
        """
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
            
        try:
            response = self._make_request("api/generate", data)
            return response.get("response", "")
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return f"Error: Failed to generate response - {str(e)}"
    


# Global Ollama API instance
ollama_api = None

def initialize_ollama(config_path: str = "app/config.json") -> bool:
    """
    Initialize Ollama API with configuration
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        True if initialization successful, False otherwise
    """
    global ollama_api
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        ollama_url = config.get("ollama_endpoint", "http://host.docker.internal:11434")
        ollama_api = OllamaAPI(ollama_url)
        
        logger.info("Ollama API initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Ollama API: {e}")
        return False

def generate_text(user_message: str, is_initial: bool = False, 
                 prompt_type: str = "general", system_prompt: str = None) -> str:
    """
    Generate text response using Ollama
    
    Args:
        user_message: User input message
        is_initial: Whether this is an initial message (unused for Ollama)
        prompt_type: Type of prompt (unused for Ollama)
        system_prompt: System prompt to use
        
    Returns:
        Generated response text
    """
    global ollama_api
    
    if ollama_api is None:
        if not initialize_ollama():
            return "Error: Ollama API not initialized"
    
    try:
        response = ollama_api.generate(user_message, system_prompt)
        return response
    except Exception as e:
        logger.error(f"Error in generate_text: {e}")
        return f"Error generating response: {str(e)}"

def test_connection() -> bool:
    """
    Test connection to Ollama server
    
    Returns:
        True if connection successful, False otherwise
    """
    global ollama_api
    
    if ollama_api is None:
        if not initialize_ollama():
            return False
    
    try:
        # Simple test by trying to generate with the model
        test_response = ollama_api.generate("test", "You are a helpful assistant.")
        return bool(test_response and not test_response.startswith("Error:"))
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
