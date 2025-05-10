import logging

from .schemas import (
    ProfileExtractRequest, 
    ProfileExtractResponse,
    GeneratePlanRequest, 
    GeneratePlanResponse
)
from .config import PlanningConfig
from .modules.profile_service import ProfileExtractionService
from .modules.plan_service import PlanGenerationService

logger = logging.getLogger(__name__)

class PlanningService:
    """Service for hybrid training planning, integrating profile extraction and plan generation."""

    def __init__(self):
        self.config = PlanningConfig()
        self.profile_service = ProfileExtractionService(config=self.config)
        self.plan_service = PlanGenerationService(config=self.config)

    async def extract_profile(self, request: ProfileExtractRequest) -> ProfileExtractResponse:
        """Extract profile data from user input and handle missing information."""
        return await self.profile_service.extract_profile(request)
        
    async def generate_plan(self, request: GeneratePlanRequest) -> GeneratePlanResponse:
        """Generate a complete training plan based on user profile."""
        return await self.plan_service.generate_plan(request)
        
    def build_next_conversation_history(self, current_history, response, follow_up_question):
        """Build conversation history for the next request."""
        return self.profile_service.build_next_conversation_history(
            current_history, response, follow_up_question
        )
