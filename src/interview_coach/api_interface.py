"""
Common API interface for both OpenAI and Gemini
"""
from typing import Dict, Any, List
from .utils import get_api_client


class AIInterface:
    """Unified interface for AI providers (OpenAI and Gemini)."""

    def __init__(self):
        self.client, self.config = get_api_client()
        self.api_provider = self.config["api_provider"]

    def generate_response(self, system_prompt: str, user_input: str) -> str:
        """Generate response using the configured AI provider."""
        if self.api_provider == "gemini":
            return self._generate_gemini_response(system_prompt, user_input)
        elif self.api_provider == "openai":
            return self._generate_openai_response(system_prompt, user_input)
        else:
            raise ValueError(f"Unsupported API provider: {self.api_provider}")

    def _generate_gemini_response(self, system_prompt: str, user_input: str) -> str:
        """Generate response using Gemini."""
        import google.generativeai as genai

        # Combine system prompt and user input
        full_prompt = f"{system_prompt}\n\nUser: {user_input}\n\nAssistant:"

        response = self.client.generate_content(
            full_prompt,
            generation_config={
                "temperature": self.config["temperature"],
            }
        )

        return response.text if response.text else "I couldn't generate a response."

    def _generate_openai_response(self, system_prompt: str, user_input: str) -> str:
        """Generate response using OpenAI."""
        from openai import OpenAI

        client = self.client  # This is the OpenAI client

        response = client.chat.completions.create(
            model=self.config["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=self.config["temperature"]
        )

        return response.choices[0].message.content