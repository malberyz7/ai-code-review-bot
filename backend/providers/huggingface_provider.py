"""HuggingFace provider implementation."""
import time
import requests
from typing import Optional
from .base import BaseAIProvider
from config import HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL


class HuggingFaceProvider(BaseAIProvider):
    """HuggingFace API provider."""
    
    def __init__(self):
        """Initialize HuggingFace provider."""
        self.api_key = HUGGINGFACE_API_KEY
        self.model = HUGGINGFACE_MODEL
        self.headers = {"Content-Type": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def analyze_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Analyze code using HuggingFace API.
        
        Args:
            code: Code snippet to analyze
            language: Optional programming language
            
        Returns:
            AI response as string
        """
        language_hint = f" (Language: {language})" if language else ""
        prompt = self._build_base_prompt(code, language, language_hint)
        hf_prompt = self._build_hf_prompt(prompt)
        
        api_url = self._find_working_endpoint()
        
        hf_response = self._make_request(api_url, hf_prompt)
        
        if hf_response.status_code == 503:
            hf_response = self._retry_after_wait(api_url, hf_prompt, hf_response)
        
        self._validate_response(hf_response)
        
        return self._extract_content(hf_response)
    
    def _build_base_prompt(self, code: str, language: Optional[str], language_hint: str) -> str:
        """Build base prompt for code review."""
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
    
    def _build_hf_prompt(self, base_prompt: str) -> str:
        """Build HuggingFace-specific prompt."""
        return f"""You are an expert code reviewer. Analyze the following code and provide a comprehensive review in JSON format.

{base_prompt}

Return ONLY valid JSON with this structure:
{{
    "summary": "brief summary",
    "issues": [{{"type": "bug", "severity": "high", "description": "...", "line": null}}],
    "suggestions": ["suggestion 1", "suggestion 2"],
    "improved_code": "improved code or null"
}}"""
    
    def _find_working_endpoint(self) -> str:
        """Find a working HuggingFace API endpoint."""
        api_urls = [
            f"https://router.huggingface.co/hf-inference/models/{self.model}",
            f"https://api-inference.huggingface.co/models/{self.model}",
        ]
        
        for url in api_urls:
            try:
                test_response = requests.post(
                    url,
                    headers=self.headers,
                    json={"inputs": "test", "parameters": {"max_new_tokens": 1}},
                    timeout=10
                )
                if test_response.status_code not in (410, 404):
                    return url
            except Exception:
                continue
        
        return api_urls[0]
    
    def _make_request(self, api_url: str, prompt: str) -> requests.Response:
        """Make request to HuggingFace API."""
        try:
            return requests.post(
                api_url,
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 2000,
                        "temperature": 0.3,
                        "return_full_text": False
                    }
                },
                timeout=90
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Hugging Face API: {str(e)}")
    
    def _retry_after_wait(
        self, api_url: str, prompt: str, response: requests.Response
    ) -> requests.Response:
        """Retry request after waiting for model to be ready."""
        error_info = (
            response.json()
            if response.headers.get('content-type', '').startswith('application/json')
            else {}
        )
        estimated_time = error_info.get("estimated_time", 15)
        time.sleep(min(estimated_time + 5, 30))
        
        try:
            return requests.post(
                api_url,
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 2000,
                        "temperature": 0.3,
                        "return_full_text": False
                    }
                },
                timeout=90
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Hugging Face API after retry: {str(e)}")
    
    def _validate_response(self, response: requests.Response):
        """Validate HuggingFace API response."""
        if response.status_code == 200:
            return
        
        error_text = response.text
        try:
            error_json = response.json()
            if isinstance(error_json, dict):
                error_text = error_json.get("error", str(error_json))
            else:
                error_text = str(error_json)
        except Exception:
            pass
        
        if response.status_code == 401:
            raise Exception(
                "Hugging Face authentication failed. Check HUGGINGFACE_API_KEY. "
                "Get token: https://huggingface.co/settings/tokens"
            )
        elif response.status_code == 403:
            raise Exception(
                "Hugging Face permission error: Token needs 'Inference API' permission. "
                "Update at: https://huggingface.co/settings/tokens"
            )
        elif response.status_code == 404:
            raise Exception(
                f"Model '{self.model}' not found. Update HUGGINGFACE_MODEL in backend/.env. "
                "Try: 'mistralai/Mistral-7B-Instruct-v0.1'"
            )
        elif response.status_code == 410:
            raise Exception(
                "Hugging Face endpoint deprecated for this model. The code will try a simpler model. "
                "If this persists, Hugging Face API may be temporarily unavailable. "
                "You can try again later or use OpenAI if you have credits."
            )
        
        raise Exception(f"Hugging Face API error (Status {response.status_code}): {error_text}")
    
    def _extract_content(self, response: requests.Response) -> str:
        """Extract content from HuggingFace API response."""
        try:
            result = response.json()
        except Exception:
            raise Exception(f"Invalid JSON response from Hugging Face API: {response.text[:200]}")
        
        if isinstance(result, list) and len(result) > 0:
            content = result[0].get("generated_text", "").strip()
        elif isinstance(result, dict):
            if "generated_text" in result:
                content = result.get("generated_text", "").strip()
            elif result and isinstance(list(result.values())[0], dict):
                content = list(result.values())[0].get("generated_text", "").strip()
            else:
                raise Exception(f"Unexpected response format: {result}")
        else:
            raise Exception(f"Unexpected response format: {result}")
        
        if not content:
            raise Exception(f"Empty response from Hugging Face API: {result}")
        
        if "<|start_header_id|>assistant<|end_header_id|>" in content:
            content = content.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
        
        return content

