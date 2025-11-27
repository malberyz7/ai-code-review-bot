"""Base class for AI providers."""
from abc import ABC, abstractmethod
from typing import Optional


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def analyze_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Analyze code and return AI response.
        
        Args:
            code: Code snippet to analyze
            language: Optional programming language
            
        Returns:
            AI response as string
        """
        pass

