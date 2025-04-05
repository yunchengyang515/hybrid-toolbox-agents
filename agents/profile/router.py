import json
from fastapi import APIRouter, HTTPException, status
import logging

from common.llm import LLMClient
from common.schemas import Message, Role
from .schemas import (
    ProfileExtractRequest, 
    ProfileExtractResponse,
)
from .services import ProfileExtractionService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/extract", response_model=ProfileExtractResponse)
async def extract_profile(request: ProfileExtractRequest):
    """Extract structured profile information from user input."""
    try:
        extraction_service = ProfileExtractionService()
        response = await extraction_service.extract_profile(request)
        return response
    except Exception as e:
        logger.error(f"Profile extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract profile: {str(e)}"
        )


