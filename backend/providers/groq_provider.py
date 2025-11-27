"""Groq provider implementation."""
import requests
from typing import Optional
from .base import BaseAIProvider
from config import GROQ_API_KEY, GROQ_MODEL


class GroqProvider(BaseAIProvider):
    """Groq API provider."""
    
    def __init__(self):
        """Initialize Groq provider."""
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Analyze code using Groq API.
        
        Args:
            code: Code snippet to analyze
            language: Optional programming language
            
        Returns:
            AI response as string
        """
        language_hint = f" (Language: {language})" if language else ""
        prompt = self._build_prompt(code, language, language_hint)
        
        response = requests.post(
            self.url,
            headers=self.headers,
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer. Always respond with valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"Groq API error: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    
    def _build_prompt(self, code: str, language: Optional[str], language_hint: str) -> str:
        """Build the prompt for code review."""
        return f"""You are an expert code reviewer. Analyze the following code{language_hint} and provide a comprehensive review.

Code to review:
```{language or ''}
{code}
```

Please provide your analysis in the following JSON format:
{{
    "summary": "A brief 2-3 sentence summary of the code and overall assessment",
    "issues": [
        {{
            "type": "bug|security|performance|quality",
            "severity": "critical|high|medium|low",
            "description": "Clear description of the issue",
            "line": "line number or range if applicable"
        }}
    ],
    "suggestions": [
        "Specific improvement suggestions",
        "Best practices recommendations",
        "Code style improvements"
    ],
    "improved_code": "An improved/optimized version of the code if significant improvements are possible, otherwise null"
}}

Focus on:
1. Code quality issues (readability, maintainability, style)
2. Bugs or logical errors
3. Security vulnerabilities
4. Performance problems
5. Best practices and improvements

Return ONLY valid JSON, no additional text."""

