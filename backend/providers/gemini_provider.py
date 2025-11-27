"""Gemini provider implementation."""
import google.generativeai as genai
from typing import Optional
from .base import BaseAIProvider
from config import GEMINI_MODEL


class GeminiProvider(BaseAIProvider):
    """Google Gemini API provider."""
    
    def __init__(self):
        """Initialize Gemini provider."""
        self.model_name = GEMINI_MODEL
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Gemini model with fallback options."""
        model_names_to_try = [
            "models/gemini-2.0-flash",
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro",
            "models/gemini-2.0-flash-exp",
        ]
        
        if self.model_name and self.model_name not in model_names_to_try:
            model_names_to_try.insert(0, self.model_name)
        elif self.model_name in model_names_to_try:
            model_names_to_try.remove(self.model_name)
            model_names_to_try.insert(0, self.model_name)
        
        last_error = None
        
        for model_name in model_names_to_try:
            try:
                self.model = genai.GenerativeModel(model_name)
                return
            except Exception as e:
                last_error = str(e)
                continue
        
        # If no model worked, try to get available models
        try:
            available_models = [
                m.name for m in genai.list_models()
                if 'generateContent' in m.supported_generation_methods
            ]
            available_str = ", ".join(available_models[:3])
            raise Exception(
                f"Gemini model not found. Available models include: {available_str}. "
                f"Update GEMINI_MODEL in backend/.env"
            )
        except Exception:
            raise Exception(
                f"Gemini model '{self.model_name}' not found. Error: {last_error}. "
                f"Try: models/gemini-2.0-flash"
            )
    
    def analyze_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Analyze code using Gemini API.
        
        Args:
            code: Code snippet to analyze
            language: Optional programming language
            
        Returns:
            AI response as string
        """
        language_hint = f" (Language: {language})" if language else ""
        prompt = self._build_prompt(code, language, language_hint)
        full_prompt = f"""You are an expert code reviewer. Always respond with valid JSON only.

{prompt}"""
        
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=2000,
                )
            )
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
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

