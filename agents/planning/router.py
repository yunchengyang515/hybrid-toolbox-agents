import json
from fastapi import APIRouter, HTTPException, status
import logging
from typing import Dict, Any

from common.llm import LLMClient
from common.schemas import Message, Role, TrainingPlan
from .schemas import (
    ProfileExtractRequest, 
    ProfileExtractResponse,
    GeneratePlanRequest,
    GeneratePlanResponse,
    ComprehensivePlanRequest,
    ComprehensivePlanResponse
)
from .services import PlanningService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate-plan-mvp", response_model=ComprehensivePlanResponse)
async def generate_comprehensive_plan(request: ComprehensivePlanRequest):
    """
    MVP endpoint that extracts profile and generates a plan in a single call.
    Takes user input directly and handles the entire flow internally.
    """
    try:
        planning_service = PlanningService()
        
        # First, extract the profile from user input
        profile_request = ProfileExtractRequest(
            user_input=request.user_input,
            conversation_history=request.conversation_history
        )
        
        profile_response = await planning_service.extract_profile(profile_request)
        logger.info(f"Profile extracted with {len(profile_response.missing_fields)} missing fields")
        
        # If profile is incomplete and follow-up questions are needed, return them
        if not profile_response.is_complete:
            return ComprehensivePlanResponse(
                status="incomplete_profile",
                profile_data=profile_response.profile_data,
                missing_fields=profile_response.missing_fields,
                follow_up_questions=profile_response.follow_up_questions,
                plan=None,
                recommendations=[]
            )
        
        # Profile is complete, so generate a plan
        plan_request = GeneratePlanRequest(
            profile=profile_response.profile_data,
            plan_parameters=request.plan_parameters
        )
        
        plan_response = await planning_service.generate_plan(plan_request)
        logger.info(f"Plan generated: {plan_response.plan.title}")
        
        return ComprehensivePlanResponse(
            status="complete",
            profile_data=profile_response.profile_data,
            missing_fields=[],
            follow_up_questions=[],
            plan=plan_response.plan,
            recommendations=plan_response.recommendations
        )
        
    except Exception as e:
        logger.error(f"Comprehensive plan generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process plan: {str(e)}"
        )

@router.post("/extract-profile", response_model=ProfileExtractResponse)
async def extract_profile(request: ProfileExtractRequest):
    """Extract structured profile information from user input."""
    try:
        planning_service = PlanningService()
        response = await planning_service.extract_profile(request)
        return response
    except Exception as e:
        logger.error(f"Profile extraction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract profile: {str(e)}"
        )

@router.post("/generate-plan", response_model=GeneratePlanResponse)
async def generate_plan(request: GeneratePlanRequest):
    """Generate a complete training plan based on user profile."""
    try:
        planning_service = PlanningService()
        response = await planning_service.generate_plan(request)
        return response
    except Exception as e:
        logger.error(f"Plan generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate plan: {str(e)}"
        )

@router.post("/example", response_model=Dict[str, Any])
async def planning_example():
    """Example of how to use the planning API in a workflow."""
    
    example = {
        "workflow_description": "Complete hybrid training planning workflow",
        "steps": [
            {
                "step": 1,
                "description": "Use the comprehensive MVP endpoint",
                "endpoint": "/v1/planning/generate-plan-mvp",
                "request_preview": {
                    "user_input": "I want to start a hybrid training program. I'm a runner who does 20 miles per week. I have access to a gym with all equipment and can train Monday, Wednesday, Friday evenings and weekends. My goal is to improve my half marathon time while building some muscle.",
                    "plan_parameters": {
                        "duration_weeks": 4,
                        "emphasis": "balanced"
                    }
                },
                "follow_up_example": {
                    "user_input": "I have a background in CrossFit from 2 years ago and I occasionally have knee pain.",
                    "conversation_history": [
                        {"role": "user", "content": "I want to start a hybrid training program. I'm a runner who does 20 miles per week. I have access to a gym with all equipment and can train Monday, Wednesday, Friday evenings and weekends. My goal is to improve my half marathon time while building some muscle."},
                        {"role": "assistant", "content": "Can you tell me about your fitness background or any health constraints I should consider for your training plan?"}
                    ],
                    "plan_parameters": {
                        "duration_weeks": 4,
                        "emphasis": "balanced"
                    }
                }
            }
        ]
    }
    return example
