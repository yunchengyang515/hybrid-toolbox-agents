from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from common.schemas import UserProfile

class ProfileExtractRequest(BaseModel):
    """Request to extract a user profile from text."""
    user_input: str = Field(..., 
                         description="The raw user input to extract profile information from")

class ProfileExtractResponse(BaseModel):
    """Response containing the extracted profile data."""
    profile_data: Dict[str, Any] = Field(..., 
                                      description="Structured profile data extracted from input")
    raw_input: str = Field(..., 
                        description="The original user input used for extraction")

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
