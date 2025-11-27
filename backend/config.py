"""Configuration management for the application."""
import os
from pathlib import Path
from dotenv import load_dotenv

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# AI Provider Configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# HuggingFace Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")


def validate_configuration():
    """Validate and configure AI provider settings."""
    if AI_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set when using OpenAI provider"
            )
        import openai
        openai.api_key = OPENAI_API_KEY

    elif AI_PROVIDER == "huggingface":
        if not HUGGINGFACE_API_KEY:
            print("⚠️  Warning: HUGGINGFACE_API_KEY not set. Using public API (may be slower).")
            print("   Get a free API key at: https://huggingface.co/settings/tokens")

    elif AI_PROVIDER == "groq":
        if not GROQ_API_KEY:
            print("   Get a free API key at: https://console.groq.com/keys")
            raise ValueError(
                "GROQ_API_KEY environment variable is not set when using Groq provider"
            )

    elif AI_PROVIDER == "gemini":
        if not GEMINI_AVAILABLE:
            raise ValueError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )
        if not GEMINI_API_KEY:
            print("   Get a free API key at: https://makersuite.google.com/app/apikey")
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set when using Gemini provider"
            )
        genai.configure(api_key=GEMINI_API_KEY)

