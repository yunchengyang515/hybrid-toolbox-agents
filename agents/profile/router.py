import json
from fastapi import APIRouter, HTTPException, status
import logging
from typing import Dict, Any

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

@router.post("/extract_example", response_model=Dict[str, Any])
async def extract_profile_example():
    """Example of how to use the profile extraction API in a conversation flow."""
    
    # This is just an example - not functional code
    example = {
        "flow_description": "How to use the profile extraction API in a conversation flow",
        "steps": [
            {
                "step": 1,
                "description": "Initial request with user input only",
                "request": {
                    "user_input": "I want to start a hybrid training program. I'm mostly a runner."
                },
                "response": {
                    "profile_data": {"training_history": "Mostly running background"},
                    "missing_fields": ["fitness_background", "training_goals", "weekly_schedule"],
                    "follow_up_questions": ["Can you tell me about your fitness background beyond running?"]
                }
            },
            {
                "step": 2,
                "description": "Follow-up request includes conversation history",
                "request": {
                    "user_input": "I played soccer in college and have done a few half marathons.",
                    "conversation_history": [
                        {"role": "user", "content": "I want to start a hybrid training program. I'm mostly a runner."},
                        {"role": "assistant", "content": "Can you tell me about your fitness background beyond running?"}
                    ]
                },
                "response": {
                    "profile_data": {
                        "training_history": "Mostly running background",
                        "fitness_background": "Played soccer in college, completed half marathons"
                    },
                    "missing_fields": ["training_goals", "weekly_schedule"],
                    "follow_up_questions": ["What are your main fitness goals with this hybrid training program?"]
                }
            }
            # Additional steps would follow the same pattern
        ]
    }
    return example


