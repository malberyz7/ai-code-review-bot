"""Custom exceptions for error handling."""
from fastapi import HTTPException


def create_quota_exception():
    """Create HTTPException for quota exceeded errors."""
    return HTTPException(
        status_code=402,
        detail={
            "error": "Gemini API Quota Exceeded",
            "message": "You have exceeded your Gemini API quota. "
                       "Please check your plan and billing details.",
            "help": "Visit https://makersuite.google.com/app/apikey "
                    "to check your API usage and limits.",
            "docs": "https://ai.google.dev/docs"
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


def create_authentication_exception():
    """Create HTTPException for authentication errors."""
    return HTTPException(
        status_code=401,
        detail={
            "error": "Gemini API Authentication Failed",
            "message": "Invalid API key. Please check your GEMINI_API_KEY "
                      "in the backend/.env file.",
            "help": "Get your API key from https://makersuite.google.com/app/apikey"
        }
    )


def create_generic_api_exception(message: str):
    """Create HTTPException for generic API errors."""
    return HTTPException(
        status_code=502,
        detail={
            "error": "Gemini API Error",
            "message": message,
            "help": "There was an issue with the Gemini API. Please try again later."
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
