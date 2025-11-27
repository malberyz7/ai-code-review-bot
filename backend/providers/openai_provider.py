"""OpenAI provider implementation."""
import openai
from typing import Optional
from .base import BaseAIProvider
from config import OPENAI_MODEL


class OpenAIProvider(BaseAIProvider):
    """OpenAI API provider."""
    
    def __init__(self):
        """Initialize OpenAI provider."""
        self.model = OPENAI_MODEL
    
    def analyze_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Analyze code using OpenAI API.
        
        Args:
            code: Code snippet to analyze
            language: Optional programming language
            
        Returns:
            AI response as string
        """
        language_hint = f" (Language: {language})" if language else ""
        prompt = self._build_prompt(code, language, language_hint)
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert code reviewer. Always respond with valid JSON only."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
    
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

