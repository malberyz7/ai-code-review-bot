"""Main FastAPI application."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from config import FRONTEND_DIR, validate_configuration
from models import CodeReviewRequest, CodeReviewResponse
from services import CodeReviewService

# Validate configuration on startup
validate_configuration()

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

# Mount static files
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Initialize service
code_review_service = CodeReviewService()


@app.get("/")
async def root():
    """Root endpoint serving frontend or API info."""
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
    """
    Review code endpoint.
    
    Args:
        request: Code review request with code and optional language
        
    Returns:
        Code review response with analysis
        
    Raises:
        HTTPException: For validation or processing errors
    """
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
        analysis = code_review_service.analyze_code(request.code, request.language)
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
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
