from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Any, Optional, Union

class Role(str, Enum):
    """Role enum for LLM message exchanges."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    
class Message(BaseModel):
    """Message schema for LLM interactions."""
    role: Role
    content: str

class ErrorResponse(BaseModel):
    """Standard error response format."""
    detail: str
    
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str = "1.0.0"

# Base user profile schemas
class UserProfile(BaseModel):
    """Base user profile information."""
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    experience_level: Optional[str] = None
    goals: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    
# Base training plan schemas
class Exercise(BaseModel):
    """Exercise schema."""
    name: str
    sets: Optional[int] = None
    reps: Optional[str] = None
    weight: Optional[str] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

class TrainingBlock(BaseModel):
    """Training block schema."""
    name: str
    description: Optional[str] = None
    exercises: List[Exercise]
    
class TrainingDay(BaseModel):
    """Training day schema."""
    day: str
    blocks: List[TrainingBlock]
    
class TrainingWeek(BaseModel):
    """Weekly training plan schema."""
    week_number: int
    days: List[TrainingDay]
    
class TrainingPlan(BaseModel):
    """Complete training plan schema."""
    title: str
    description: str
    weeks: List[TrainingWeek]
    notes: Optional[str] = None
