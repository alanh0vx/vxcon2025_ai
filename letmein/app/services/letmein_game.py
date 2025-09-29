from app.services.llm_api import generate_text
from app.services.system_prompts import SystemPrompts
import json
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LetMeInGame:
    def __init__(self, wordlist_file: str = "app/wordlist.json"):
        """
        Initialize the Let Me In game
        
        Args:
            wordlist_file: Path to wordlist JSON file
        """
        self.wordlist_file = wordlist_file
        self.wordlist = self.load_wordlist()
        self.passwords = self.generate_passwords()
        self.current_level = 1
        self.max_level = 4
        
    def load_wordlist(self) -> list:
        """
        Load wordlist from JSON file
        
        Returns:
            List of words for password generation
        """
        try:
            with open(self.wordlist_file, 'r') as f:
                data = json.load(f)
            return data.get('wordlist', [])
        except FileNotFoundError:
            logger.error(f"Wordlist file not found: {self.wordlist_file}")
            return ["letmein", "password", "admin", "secret"]
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in wordlist file: {self.wordlist_file}")
            return ["letmein", "password", "admin", "secret"]
    
    def generate_passwords(self) -> dict:
        """
        Generate random passwords for all levels using wordlist
        
        Returns:
            Dictionary containing generated passwords
        """
        passwords = {}
        used = set()
        
        # Get all levels from system prompts
        levels = sorted(SystemPrompts.letmein_game.keys())  # ['lv1', 'lv2', 'lv3', 'lv4']
        
        for key in levels:
            attempts = 0
            while attempts < 100:  # Prevent infinite loop
                candidate = random.choice(self.wordlist) + str(random.randint(10, 99))
                if candidate not in used:
                    used.add(candidate)
                    passwords[key] = candidate
                    break
                attempts += 1
            
            # Fallback if no unique password found
            if key not in passwords:
                passwords[key] = f"fallback{random.randint(1000, 9999)}"
        
        logger.info(f"Generated passwords: {passwords}")
        return passwords
    
    def check_password(self, level: int, user_input: str) -> bool:
        """
        Check if user input contains the correct password
        
        Args:
            level: Game level
            user_input: User's input or LLM response
            
        Returns:
            True if password found, False otherwise
        """
        level_key = f"lv{level}"
        if level_key not in self.passwords:
            return False
        
        correct_password = self.passwords[level_key]
        return correct_password.lower() in user_input.lower()
    
    def get_letmein_response(self, level: int, user_message: str) -> str:
        """
        Get AI response for Let Me In game at the given level
        
        Args:
            level: Game level (1-4)
            user_message: User's message to the AI
            
        Returns:
            AI response string
        """
        level_key = f"lv{level}"
        
        # Get system prompt for this level
        base_prompt = SystemPrompts.letmein_game.get(level_key)
        if not base_prompt:
            return f"Error: Invalid game level '{level_key}'. No matching prompt found."
        
        if level_key not in self.passwords:
            return f"Error: Password for level {level} not found."
        
        # Inject the password into the system prompt
        password = self.passwords[level_key]
        system_prompt = base_prompt.replace(f"[LETMEIN_LV{level}_PASS]", password)
        
        # Generate response using LLM
        try:
            response = generate_text(
                user_message,
                is_initial=False,
                prompt_type="letmein_game",
                system_prompt=system_prompt
            )
            return response
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return f"Error: Failed to generate response - {str(e)}"

# Legacy function for backward compatibility
def get_letmein_prompts(level: int, user_message: str, passwords: dict) -> str:
    """
    Generates the AI response for Let Me In game at the given level (lv1+),
    injecting the dynamic password into the system prompt.
    """
    key = f"lv{level}"

    base_prompt = SystemPrompts.letmein_game.get(key)
    if not base_prompt:
        return f"Error: Invalid game level '{key}'. No matching prompt found."

    if key not in passwords:
        return f"Error: Password for level {level} not found."

    password = passwords[key]
    prompt = base_prompt.replace(f"[LETMEIN_LV{level}_PASS]", password)

    response = generate_text(
        user_message,
        is_initial=False,
        prompt_type="letmein_game",
        system_prompt=prompt
    )

    return response