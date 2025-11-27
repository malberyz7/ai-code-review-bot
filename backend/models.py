"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional


class CodeReviewRequest(BaseModel):
    """Request model for code review endpoint."""
    code: str = Field(..., description="The code snippet to review", min_length=1)
    language: Optional[str] = Field(
        None, description="Programming language (optional, will be auto-detected)"
    )


class CodeReviewResponse(BaseModel):
    """Response model for code review endpoint."""
    summary: str
    issues: list
    suggestions: list
    improved_code: Optional[str] = None

