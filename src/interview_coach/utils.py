"""
Utility functions for the AI Interview Coach
"""
import os
from typing import Optional
from dotenv import load_dotenv


def load_api_config():
    """Load API configuration from environment variables."""
    load_dotenv()

    # Try Gemini first, then OpenAI
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return {
            "api_provider": "gemini",
            "api_key": api_key,
            "model": os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7"))
        }

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return {
            "api_provider": "openai",
            "api_key": api_key,
            "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7"))
        }

    raise ValueError("Either GEMINI_API_KEY or OPENAI_API_KEY environment variable is required")


def get_api_client():
    """Get the appropriate API client based on configuration."""
    config = load_api_config()

    if config["api_provider"] == "gemini":
        try:
            import google.generativeai as genai
            genai.configure(api_key=config["api_key"])
            return genai.GenerativeModel(config["model"]), config
        except ImportError:
            raise ImportError("Please install google-generativeai: pip install google-generativeai")

    elif config["api_provider"] == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=config["api_key"])
            return client, config
        except ImportError:
            raise ImportError("Please install openai: pip install openai")

    else:
        raise ValueError(f"Unsupported API provider: {config['api_provider']}")


def format_large_text(text: str, max_length: int = 1000) -> str:
    """Format large text for display, truncating if necessary."""
    if len(text) <= max_length:
        return text

    return text[:max_length] + "... [truncated]"


def sanitize_input(user_input: str) -> str:
    """Sanitize user input by removing potentially harmful content."""
    # Remove excessive whitespace
    sanitized = ' '.join(user_input.split())

    # Remove potentially harmful patterns (basic sanitization)
    harmful_patterns = [
        '<script', 'javascript:', 'vbscript:', 'onerror=', 'onload=',
        'document.cookie', 'window.location'
    ]

    for pattern in harmful_patterns:
        if pattern.lower() in sanitized.lower():
            sanitized = sanitized.replace(pattern, '[filtered]')

    return sanitized


def validate_job_description(description: str) -> tuple[bool, str]:
    """Validate job description input."""
    if not description or len(description.strip()) < 10:
        return False, "Job description is too short. Please provide more details."

    if len(description) > 10000:
        return False, "Job description is too long. Please provide a concise version (under 10,000 characters)."

    return True, ""


def validate_resume(resume: str) -> tuple[bool, str]:
    """Validate resume input."""
    if not resume or len(resume.strip()) < 10:
        return False, "Resume is too short. Please provide more details about your background."

    if len(resume) > 10000:
        return False, "Resume is too long. Please provide a concise version (under 10,000 characters)."

    return True, ""