"""Code review service."""
import json
from typing import Optional, Dict, Any
from providers import (
    OpenAIProvider,
    HuggingFaceProvider,
    GroqProvider,
    GeminiProvider,
    BaseAIProvider
)
from config import AI_PROVIDER
from exceptions import (
    create_quota_exception,
    create_rate_limit_exception,
    create_authentication_exception,
    create_generic_api_exception,
    create_unexpected_exception,
)


class CodeReviewService:
    """Service for analyzing code using AI providers."""
    
    def __init__(self):
        """Initialize code review service with appropriate provider."""
        self.provider = self._get_provider()
    
    def _get_provider(self) -> BaseAIProvider:
        """Get the appropriate AI provider based on configuration."""
        provider_map = {
            "openai": OpenAIProvider,
            "huggingface": HuggingFaceProvider,
            "groq": GroqProvider,
            "gemini": GeminiProvider,
        }
        
        provider_class = provider_map.get(AI_PROVIDER)
        if not provider_class:
            raise ValueError(f"Unknown AI provider: {AI_PROVIDER}")
        
        return provider_class()
    
    def analyze_code(
        self, code: str, language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze code and return structured review.
        
        Args:
            code: Code snippet to analyze
            language: Optional programming language
            
        Returns:
            Dictionary with summary, issues, suggestions, and improved_code
            
        Raises:
            HTTPException: For various error conditions
        """
        try:
            content = self.provider.analyze_code(code, language)
            content = self._clean_content(content)
            analysis = json.loads(content)
            
            return {
                "summary": analysis.get("summary", "Analysis completed."),
                "issues": analysis.get("issues", []),
                "suggestions": analysis.get("suggestions", []),
                "improved_code": analysis.get("improved_code")
            }
            
        except json.JSONDecodeError as e:
            return {
                "summary": "Analysis completed, but response formatting encountered an issue.",
                "issues": [{
                    "type": "error",
                    "severity": "medium",
                    "description": f"Failed to parse AI response: {str(e)}",
                    "line": None
                }],
                "suggestions": ["Please try reviewing the code again."],
                "improved_code": None
            }
        except Exception as e:
            self._handle_exception(e)
    
    def _clean_content(self, content: str) -> str:
        """Clean AI response content."""
        if content.startswith("```"):
            content = content.strip("```json").strip("```").strip()
        return content
    
    def _handle_exception(self, error: Exception):
        """Handle exceptions and convert to appropriate HTTPException."""
        error_msg = str(error).lower()
        
        if any(keyword in error_msg for keyword in ["quota", "billing", "exceeded"]):
            raise create_quota_exception()
        
        if any(keyword in error_msg for keyword in ["rate limit", "too many requests"]):
            raise create_rate_limit_exception()
        
        if (
            "authentication" in error_msg
            or ("invalid" in error_msg and "key" in error_msg)
            or "unauthorized" in error_msg
        ):
            raise create_authentication_exception(AI_PROVIDER)
        
        if "api error" in error_msg or "api" in error_msg:
            raise create_generic_api_exception(str(error))
        
        raise create_unexpected_exception(str(error))

