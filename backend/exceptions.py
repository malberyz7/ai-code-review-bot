"""Custom exceptions for error handling."""
from fastapi import HTTPException


class AIProviderError(HTTPException):
    """Base exception for AI provider errors."""
    pass


def create_quota_exception():
    """Create HTTPException for quota exceeded errors."""
    return HTTPException(
        status_code=402,
        detail={
            "error": "OpenAI API Quota Exceeded",
            "message": "You have exceeded your OpenAI API quota. "
                       "Please check your plan and billing details.",
            "help": "Visit https://platform.openai.com/account/billing "
                    "to add credits or upgrade your plan.",
            "docs": "https://platform.openai.com/docs/guides/error-codes/api-errors"
        }
    )


def create_rate_limit_exception():
    """Create HTTPException for rate limit errors."""
    return HTTPException(
        status_code=429,
        detail={
            "error": "Rate Limit Exceeded",
            "message": "Too many requests. Please wait a moment and try again.",
            "help": "The API has rate limits. Please wait before making another request."
        }
    )


def create_authentication_exception(provider: str):
    """Create HTTPException for authentication errors."""
    provider_configs = {
        "openai": ("OpenAI", "OPENAI_API_KEY", "https://platform.openai.com/api-keys"),
        "huggingface": (
            "Hugging Face", "HUGGINGFACE_API_KEY",
            "https://huggingface.co/settings/tokens"
        ),
        "groq": ("Groq", "GROQ_API_KEY", "https://console.groq.com/keys"),
        "gemini": (
            "Google Gemini", "GEMINI_API_KEY",
            "https://makersuite.google.com/app/apikey"
        ),
    }
    
    provider_name, key_name, help_url = provider_configs.get(
        provider, ("Unknown", "API_KEY", "")
    )
    
    return HTTPException(
        status_code=401,
        detail={
            "error": f"{provider_name} API Authentication Failed",
            "message": f"Invalid API key. Please check your {key_name} "
                      f"in the backend/.env file.",
            "help": f"Get your API key from {help_url}"
        }
    )


def create_generic_api_exception(message: str):
    """Create HTTPException for generic API errors."""
    return HTTPException(
        status_code=502,
        detail={
            "error": "OpenAI API Error",
            "message": message,
            "help": "There was an issue with the OpenAI API. Please try again later."
        }
    )


def create_unexpected_exception(message: str):
    """Create HTTPException for unexpected errors."""
    return HTTPException(
        status_code=500,
        detail={
            "error": "Unexpected Error",
            "message": f"An unexpected error occurred: {message}",
            "help": "Please check the server logs for more details."
        }
    )

