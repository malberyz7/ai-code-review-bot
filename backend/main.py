from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import openai
import requests

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

load_dotenv()

app = FastAPI(
    title="AI Code Review Bot",
    description="An AI-powered code review service that analyzes code for quality, bugs, security, and performance issues",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
if AI_PROVIDER == "openai":
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set when using OpenAI provider")
    openai.api_key = OPENAI_API_KEY

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")
if AI_PROVIDER == "huggingface":
    if not HUGGINGFACE_API_KEY:
        print("⚠️  Warning: HUGGINGFACE_API_KEY not set. Using public API (may be slower).")
        print("   Get a free API key at: https://huggingface.co/settings/tokens")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
if AI_PROVIDER == "groq":
    if not GROQ_API_KEY:
        print("   Get a free API key at: https://console.groq.com/keys")
        raise ValueError("GROQ_API_KEY environment variable is not set when using Groq provider")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")
if AI_PROVIDER == "gemini":
    if not GEMINI_AVAILABLE:
        raise ValueError("google-generativeai package not installed. Run: pip install google-generativeai")
    if not GEMINI_API_KEY:
        print("   Get a free API key at: https://makersuite.google.com/app/apikey")
        raise ValueError("GEMINI_API_KEY environment variable is not set when using Gemini provider")
    genai.configure(api_key=GEMINI_API_KEY)


class CodeReviewRequest(BaseModel):
    code: str = Field(..., description="The code snippet to review", min_length=1)
    language: Optional[str] = Field(None, description="Programming language (optional, will be auto-detected)")


class CodeReviewResponse(BaseModel):
    summary: str
    issues: list
    suggestions: list
    improved_code: Optional[str] = None


def analyze_code_with_ai(code: str, language: Optional[str] = None) -> dict:
    language_hint = f" (Language: {language})" if language else ""
    prompt = f"""You are an expert code reviewer. Analyze the following code{language_hint} and provide a comprehensive review.

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

    try:
        if AI_PROVIDER == "openai":
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            content = response.choices[0].message.content.strip()
            
        elif AI_PROVIDER == "huggingface":
            headers = {"Content-Type": "application/json"}
            if HUGGINGFACE_API_KEY:
                headers["Authorization"] = f"Bearer {HUGGINGFACE_API_KEY}"
            
            hf_prompt = f"""You are an expert code reviewer. Analyze the following code and provide a comprehensive review in JSON format.

{prompt}

Return ONLY valid JSON with this structure:
{{
    "summary": "brief summary",
    "issues": [{{"type": "bug", "severity": "high", "description": "...", "line": null}}],
    "suggestions": ["suggestion 1", "suggestion 2"],
    "improved_code": "improved code or null"
}}"""
            
            api_urls = [
                f"https://router.huggingface.co/hf-inference/models/{HUGGINGFACE_MODEL}",
                f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
            ]
            
            api_url = None
            hf_response = None
            
            for url in api_urls:
                try:
                    test_response = requests.post(
                        url,
                        headers=headers,
                        json={"inputs": "test", "parameters": {"max_new_tokens": 1}},
                        timeout=10
                    )
                    if test_response.status_code != 410 and test_response.status_code != 404:
                        api_url = url
                        break
                except:
                    continue
            
            if not api_url:
                api_url = api_urls[0]
            
            try:
                hf_response = requests.post(
                    api_url,
                    headers=headers,
                    json={"inputs": hf_prompt, "parameters": {"max_new_tokens": 2000, "temperature": 0.3, "return_full_text": False}},
                    timeout=90
                )
            except requests.exceptions.RequestException as e:
                raise Exception(f"Failed to connect to Hugging Face API: {str(e)}")
            
            if hf_response.status_code == 503:
                import time
                error_info = hf_response.json() if hf_response.headers.get('content-type', '').startswith('application/json') else {}
                estimated_time = error_info.get("estimated_time", 15)
                time.sleep(min(estimated_time + 5, 30))
                
                try:
                    hf_response = requests.post(
                        api_url,
                        headers=headers,
                        json={"inputs": hf_prompt, "parameters": {"max_new_tokens": 2000, "temperature": 0.3, "return_full_text": False}},
                        timeout=90
                    )
                except requests.exceptions.RequestException as e:
                    raise Exception(f"Failed to connect to Hugging Face API after retry: {str(e)}")
            
            if hf_response.status_code != 200:
                error_text = hf_response.text
                try:
                    error_json = hf_response.json()
                    if isinstance(error_json, dict):
                        error_text = error_json.get("error", str(error_json))
                    else:
                        error_text = str(error_json)
                except:
                    pass
                
                if hf_response.status_code == 401:
                    raise Exception(f"Hugging Face authentication failed. Check HUGGINGFACE_API_KEY. Get token: https://huggingface.co/settings/tokens")
                elif hf_response.status_code == 403:
                    raise Exception(f"Hugging Face permission error: Token needs 'Inference API' permission. Update at: https://huggingface.co/settings/tokens")
                elif hf_response.status_code == 404:
                    raise Exception(f"Model '{HUGGINGFACE_MODEL}' not found. Update HUGGINGFACE_MODEL in backend/.env. Try: 'mistralai/Mistral-7B-Instruct-v0.1'")
                elif hf_response.status_code == 410:
                    raise Exception(f"Hugging Face endpoint deprecated for this model. The code will try a simpler model. If this persists, Hugging Face API may be temporarily unavailable. You can try again later or use OpenAI if you have credits.")
                
                raise Exception(f"Hugging Face API error (Status {hf_response.status_code}): {error_text}")
            
            try:
                result = hf_response.json()
            except:
                raise Exception(f"Invalid JSON response from Hugging Face API: {hf_response.text[:200]}")
            
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
                
        elif AI_PROVIDER == "groq":
            groq_url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            groq_response = requests.post(
                groq_url,
                headers=headers,
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are an expert code reviewer. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                },
                timeout=60
            )
            
            if groq_response.status_code != 200:
                raise Exception(f"Groq API error: {groq_response.text}")
            
            result = groq_response.json()
            content = result["choices"][0]["message"]["content"].strip()
            
        elif AI_PROVIDER == "gemini":
            model_names_to_try = [
                "models/gemini-2.0-flash",
                "models/gemini-2.5-flash",
                "models/gemini-2.5-pro",
                "models/gemini-2.0-flash-exp",
            ]
            
            if GEMINI_MODEL and GEMINI_MODEL not in model_names_to_try:
                model_names_to_try.insert(0, GEMINI_MODEL)
            elif GEMINI_MODEL in model_names_to_try:
                model_names_to_try.remove(GEMINI_MODEL)
                model_names_to_try.insert(0, GEMINI_MODEL)
            
            model = None
            last_error = None
            
            for model_name in model_names_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    break
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if model is None:
                try:
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    available_str = ", ".join(available_models[:3])
                    raise Exception(f"Gemini model not found. Available models include: {available_str}. Update GEMINI_MODEL in backend/.env")
                except:
                    raise Exception(f"Gemini model '{GEMINI_MODEL}' not found. Error: {last_error}. Try: models/gemini-2.0-flash")
            
            full_prompt = f"""You are an expert code reviewer. Always respond with valid JSON only.

{prompt}"""
            
            try:
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3,
                        max_output_tokens=2000,
                    )
                )
                content = response.text.strip()
            except Exception as e:
                raise Exception(f"Gemini API error: {str(e)}")
        else:
            raise ValueError(f"Unknown AI provider: {AI_PROVIDER}")
        
        if content.startswith("```"):
            content = content.strip("```json").strip("```").strip()
        
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
        error_msg = str(e).lower()
        
        if "quota" in error_msg or "billing" in error_msg or "exceeded" in error_msg:
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "OpenAI API Quota Exceeded",
                    "message": "You have exceeded your OpenAI API quota. Please check your plan and billing details.",
                    "help": "Visit https://platform.openai.com/account/billing to add credits or upgrade your plan.",
                    "docs": "https://platform.openai.com/docs/guides/error-codes/api-errors"
                }
            )
        elif "rate limit" in error_msg or "too many requests" in error_msg:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate Limit Exceeded",
                    "message": "Too many requests. Please wait a moment and try again.",
                    "help": "The API has rate limits. Please wait before making another request."
                }
            )
        elif "authentication" in error_msg or ("invalid" in error_msg and "key" in error_msg) or "unauthorized" in error_msg:
            if AI_PROVIDER == "openai":
                provider_name, key_name, help_url = "OpenAI", "OPENAI_API_KEY", "https://platform.openai.com/api-keys"
            elif AI_PROVIDER == "huggingface":
                provider_name, key_name, help_url = "Hugging Face", "HUGGINGFACE_API_KEY", "https://huggingface.co/settings/tokens"
            elif AI_PROVIDER == "groq":
                provider_name, key_name, help_url = "Groq", "GROQ_API_KEY", "https://console.groq.com/keys"
            elif AI_PROVIDER == "gemini":
                provider_name, key_name, help_url = "Google Gemini", "GEMINI_API_KEY", "https://makersuite.google.com/app/apikey"
            else:
                provider_name, key_name, help_url = "Unknown", "API_KEY", ""
            
            raise HTTPException(
                status_code=401,
                detail={
                    "error": f"{provider_name} API Authentication Failed",
                    "message": f"Invalid API key. Please check your {key_name} in the backend/.env file.",
                    "help": f"Get your API key from {help_url}"
                }
            )
        else:
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "OpenAI API Error",
                    "message": str(e),
                    "help": "There was an issue with the OpenAI API. Please try again later."
                }
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Unexpected Error",
                "message": f"An unexpected error occurred: {str(e)}",
                "help": "Please check the server logs for more details."
            }
        )


@app.get("/")
async def root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {
        "message": "AI Code Review Bot API",
        "status": "running",
        "endpoints": {
            "review": "/review_code",
            "docs": "/docs"
        }
    }


@app.post("/review_code", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    if not request.code or not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty. Please provide a code snippet to review."
        )
    
    if len(request.code) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Code snippet is too long. Maximum length is 10,000 characters."
        )
    
    try:
        analysis = analyze_code_with_ai(request.code, request.language)
        
        return CodeReviewResponse(**analysis)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

