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

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")


def validate_configuration():
    """Validate and configure Gemini settings."""
    if not GEMINI_AVAILABLE:
        raise ValueError(
            "google-generativeai package not installed. "
            "Run: pip install google-generativeai"
        )
    
    if not GEMINI_API_KEY:
        print("   Get a free API key at: https://makersuite.google.com/app/apikey")
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Please set it in backend/.env file"
        )
    
    genai.configure(api_key=GEMINI_API_KEY)
