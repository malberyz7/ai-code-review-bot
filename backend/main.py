"""
AI Code Review Bot - Backend API
Uses FastAPI to provide code review functionality via OpenAI API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
import json
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Review Bot",
    description="An AI-powered code review service that analyzes code for quality, bugs, security, and performance issues",
    version="1.0.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY


class CodeReviewRequest(BaseModel):
    """Request model for code review"""
    code: str = Field(..., description="The code snippet to review", min_length=1)
    language: Optional[str] = Field(None, description="Programming language (optional, will be auto-detected)")


class CodeReviewResponse(BaseModel):
    """Response model for code review"""
    summary: str
    issues: list
    suggestions: list
    improved_code: Optional[str] = None


def analyze_code_with_ai(code: str, language: Optional[str] = None) -> dict:
    """
    Send code to OpenAI API for analysis
    
    Args:
        code: The code snippet to analyze
        language: Optional programming language hint
    
    Returns:
        Dictionary with analysis results
    """
    # Construct the prompt for the AI
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
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Using GPT-4 for better code analysis
            messages=[
                {"role": "system", "content": "You are an expert code reviewer. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent, focused analysis
            max_tokens=2000
        )
        
        # Extract the response content
        content = response.choices[0].message.content.strip()
        
        # Try to parse JSON from the response
        # Sometimes the response might have markdown code blocks
        if content.startswith("```"):
            # Remove markdown code block markers
            content = content.strip("```json").strip("```").strip()
        
        analysis = json.loads(content)
        
        # Validate and structure the response
        return {
            "summary": analysis.get("summary", "Analysis completed."),
            "issues": analysis.get("issues", []),
            "suggestions": analysis.get("suggestions", []),
            "improved_code": analysis.get("improved_code")
        }
        
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return a structured error response
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
        # Handle other API errors
        raise HTTPException(
            status_code=500,
            detail=f"Error calling OpenAI API: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint - health check"""
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
    """
    Main endpoint to review code
    
    Args:
        request: CodeReviewRequest containing code and optional language
    
    Returns:
        CodeReviewResponse with analysis results
    
    Raises:
        HTTPException: For invalid input or API errors
    """
    # Validate input
    if not request.code or not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty. Please provide a code snippet to review."
        )
    
    # Check code length (reasonable limit to prevent abuse)
    if len(request.code) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Code snippet is too long. Maximum length is 10,000 characters."
        )
    
    try:
        # Analyze code with AI
        analysis = analyze_code_with_ai(request.code, request.language)
        
        return CodeReviewResponse(**analysis)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

