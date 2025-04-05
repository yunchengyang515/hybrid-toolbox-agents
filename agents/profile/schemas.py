from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from common.schemas import UserProfile

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
    follow_up_question: Optional[str] = Field(default=None,
                                         description="Question to ask to get missing fitness information")

class ProfileValidateRequest(BaseModel):
    """Request to validate a user profile."""
    profile_data: Dict[str, Any] = Field(..., 
                                      description="The profile data to validate")

class ProfileValidateResponse(BaseModel):
    """Response after validation of a user profile."""
    validated_profile: Dict[str, Any] = Field(..., 
                                          description="The validated and possibly enhanced profile")
    is_valid: bool = Field(..., 
                        description="Whether the profile is valid")
    missing_fields: List[str] = Field(default_factory=list, 
                                  description="List of fields that are missing from the profile")
