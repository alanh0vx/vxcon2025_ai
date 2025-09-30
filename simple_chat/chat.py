#!/usr/bin/env python3
"""
Simple Console LLM Chatbot - Chef Assistant
A console-based chatbot that role-plays as a chef using Ollama and gemma3:270m
"""

import os
import sys
import signal
import requests
import json
from typing import Optional
from system_prompts import CHEF_SYSTEM_PROMPT, WELCOME_PROMPT_TEMPLATE


class ChefChatbot:
    def __init__(self):
        self.ollama_endpoint = os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434')
        self.model_name = os.getenv('MODEL_NAME', 'gemma3:270m')
        self.user_name = ""
        self.system_prompt = CHEF_SYSTEM_PROMPT

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n\nGoodbye {self.user_name}! Happy cooking!")
        sys.exit(0)

    def send_message(self, message: str) -> Optional[str]:
        """Send a message to the LLM and get response"""
        try:
            full_prompt = f"{self.system_prompt}\n\nUser's name: {self.user_name}\nUser: {message}\nChef Marco:"
            
            response = requests.post(
                f"{self.ollama_endpoint}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                },
                timeout=300
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                print(f"Error: HTTP {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return None

    def get_user_name(self) -> str:
        """Get the user's name"""
        while True:
            name = input("Hello! What's your name? ").strip()
            if name:
                return name
            print("Please enter your name to continue.")

    def generate_welcome_message(self) -> str:
        """Generate a personalized welcome message using the LLM"""
        try:
            welcome_prompt = WELCOME_PROMPT_TEMPLATE.format(user_name=self.user_name)
            
            response = requests.post(
                f"{self.ollama_endpoint}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": welcome_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "max_tokens": 200
                    }
                },
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                # Fallback to simple welcome if LLM fails
                return f"Hello {self.user_name}! I'm Chef Marco, ready to help you with all your cooking questions!"
                
        except requests.RequestException:
            # Fallback to simple welcome if connection fails
            return f"Hello {self.user_name}! I'm Chef Marco, ready to help you with all your cooking questions!"

    def print_welcome(self):
        """Print welcome message"""
        print("=" * 60)
        print("Welcome to Chef Marco's Kitchen!")
        print("=" * 60)
        print()
        
        # Generate personalized welcome message
        print("Generating personalized welcome...")
        welcome_msg = self.generate_welcome_message()
        print(f"{welcome_msg}")
        
        print()
        print("Press Ctrl+C anytime to exit.")
        print("-" * 60)

    def run(self):
        """Main chat loop"""
        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("Connecting to Ollama...")
        
        # Get user name
        self.user_name = self.get_user_name()
        
        # Print welcome message
        self.print_welcome()
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input(f"\n{self.user_name}: ").strip()
                
                if not user_input:
                    continue
                
                # Send message to LLM
                print("Chef Marco is thinking...")
                response = self.send_message(user_input)
                
                if response:
                    print(f"\nChef Marco: {response}")
                else:
                    print("Sorry, I couldn't process your message. Please try again.")
                    
            except EOFError:
                # Handle Ctrl+D
                break
            except KeyboardInterrupt:
                # Handle Ctrl+C (should be caught by signal handler)
                break
        
        print(f"\n\nGoodbye {self.user_name}! Happy cooking!")


if __name__ == "__main__":
    chatbot = ChefChatbot()
    chatbot.run()