from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Literal
from common.schemas import UserProfile, TrainingPlan

# Profile extraction schemas (moved from profile agent)
class ProfileExtractRequest(BaseModel):
    """Request to extract a user profile from text."""
    user_input: str = Field(..., 
                         description="The raw user input to extract profile information from")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default=None,
                                                   description="Previous messages in conversation format [{role: content}]")

class ProfileExtractResponse(BaseModel):
    """Response containing the extracted profile data."""
    profile_data: Dict[str, Any] = Field(..., 
                                      description="Structured fitness profile data extracted from input")
    raw_input: str = Field(..., 
                        description="The original user input used for extraction")
    missing_fields: List[str] = Field(default_factory=list,
                                  description="Fields that are missing from the fitness profile")
    is_complete: bool = Field(default=False,
                           description="Whether the profile has all required fitness information")
    follow_up_questions: List[str] = Field(default_factory=list,
                                     description="Questions to ask to get missing information")

# Plan generation schemas
class PlanParameters(BaseModel):
    """Parameters for plan generation."""
    duration_weeks: int = Field(default=4, description="Duration of plan in weeks")
    emphasis: str = Field(default="balanced", description="Training emphasis (e.g., running, strength, balanced)")

class GeneratePlanRequest(BaseModel):
    """Request to generate a training plan."""
    profile: Dict[str, Any] = Field(..., description="Complete user profile data")
    plan_parameters: Optional[PlanParameters] = Field(default_factory=PlanParameters, 
                                                 description="Parameters for plan generation")

class GeneratePlanResponse(BaseModel):
    """Response containing a generated training plan."""
    plan: TrainingPlan = Field(..., description="The generated training plan")
    profile_summary: Dict[str, Any] = Field(..., description="Summary of the profile used")
    recommendations: List[str] = Field(default_factory=list, 
                                  description="Additional recommendations based on the plan")
    guidelines: Optional[str] = Field(default=None, 
                                 description="Conversational guidelines for the training plan")

# Comprehensive MVP endpoint schemas that combines profile extraction and plan generation
class ComprehensivePlanRequest(BaseModel):
    """Request for the MVP endpoint that handles the entire flow."""
    user_input: str = Field(..., 
                       description="The raw user input to extract profile information from")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default=None,
                                                  description="Previous messages in conversation format [{role: content}]")
    plan_parameters: Optional[PlanParameters] = Field(default_factory=PlanParameters, 
                                                description="Parameters for plan generation")

class ComprehensivePlanResponse(BaseModel):
    """Response from the MVP endpoint with conditionally populated fields."""
    status: Literal["incomplete_profile", "complete"] = Field(...,
                                                         description="Status of the request processing")
    profile_data: Dict[str, Any] = Field(...,
                                     description="Structured fitness profile data extracted from input")
    missing_fields: List[str] = Field(default_factory=list,
                                 description="Fields that are missing from the fitness profile")
    follow_up_questions: List[str] = Field(default_factory=list,
                                      description="Questions to ask to get missing information")
    plan: Optional[TrainingPlan] = Field(default=None,
                                    description="The generated training plan (if profile is complete)")
    recommendations: List[str] = Field(default_factory=list,
                                  description="Additional recommendations based on the plan")
    guidelines: Optional[str] = Field(default=None, 
                                 description="Conversational plan guidelines (if profile is complete)")
