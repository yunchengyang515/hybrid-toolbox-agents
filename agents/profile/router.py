import json
from fastapi import APIRouter, HTTPException, status
import logging

from common.llm import LLMClient
from common.schemas import Message, Role
from .schemas import (
    ProfileExtractRequest, 
    ProfileExtractResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/extract", response_model=ProfileExtractResponse)
async def extract_profile(request: ProfileExtractRequest):
    """Extract structured profile information from user input."""
    try:
        llm = LLMClient()
        
        # Prepare messages for LLM
        system_prompt = """You are a fitness profile extraction agent. 
        Extract structured profile information from the user's text including:
        age, gender, height, weight, experience level, fitness goals, and any constraints.
        Return ONLY a JSON object with these fields and no additional text."""
        
        messages = [
            Message(role=Role.SYSTEM, content=system_prompt),
            Message(role=Role.USER, content=request.user_input)
        ]
        
        # Get LLM response
        result = await llm.generate(messages)
        result = result.strip()
        # Validate JSON response
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from LLM")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON response from LLM"
            )
        
        return ProfileExtractResponse(
            profile_data=result,
            raw_input=request.user_input
        )
    except Exception as e:
        logger.error(f"Profile extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract profile: {str(e)}"
        )


