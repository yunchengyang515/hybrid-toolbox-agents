import json
import logging
from typing import List, Dict, Any, Optional

from common.llm import LLMClient
from common.schemas import Message, Role
from .schemas import ProfileExtractRequest, ProfileExtractResponse

logger = logging.getLogger(__name__)

class ProfileExtractionService:
    """Service for extracting user profile information."""
    
    def __init__(self):
        self.required_fields = [
            "training_history", 
            "fitness_background", 
            "weekly_schedule", 
            "available_equipment",
            "fitness_goals",
            "health_constraints"
        ]
        self.llm = LLMClient()
    
    async def extract_profile(self, request: ProfileExtractRequest) -> ProfileExtractResponse:
        """Extract profile data from user input and handle missing information."""
        # Prepare messages for LLM
        system_prompt = """You are a fitness profile extraction agent specialized in understanding fitness needs.
        Extract structured profile information from the user's text including:
        - training_history (past workout experience)
        - fitness_background (athletic history, sports played)
        - weekly_schedule (days/times available for workouts)
        - available_equipment (home gym equipment, gym access)
        - fitness_goals (strength, weight loss, etc.)
        - health_constraints (injuries, conditions)
        
        Return a JSON object with these fields and also include a "missing_fields" array 
        listing any required fields that couldn't be extracted or need clarification."""
        
        # Build conversation history
        messages = [Message(role=Role.SYSTEM, content=system_prompt)]
        if request.conversation_history:
            for msg in request.conversation_history:
                role = Role.USER if msg.get("role") == "user" else Role.ASSISTANT
                messages.append(Message(role=role, content=msg.get("content", "")))
        messages.append(Message(role=Role.USER, content=request.user_input))
        
        # Get LLM response
        result = await self.llm.generate(messages)
        result = result.strip()
        
        # Validate JSON response
        try:
            parsed_result = json.loads(result)
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from LLM")
            parsed_result = {}
        
        # Extract missing fields
        missing_fields = parsed_result.pop("missing_fields", []) if isinstance(parsed_result, dict) else []
        for field in self.required_fields:
            if field not in parsed_result or not parsed_result.get(field):
                if field not in missing_fields:
                    missing_fields.append(field)
        
        # Check if profile is complete
        is_complete = len(missing_fields) == 0
        
        # Generate follow-up question if needed
        follow_up_question = None
        if not is_complete:
            follow_up_question = await self._generate_follow_up_question(missing_fields)
        
        return ProfileExtractResponse(
            profile_data=parsed_result,
            raw_input=request.user_input,
            missing_fields=missing_fields,
            is_complete=is_complete,
            follow_up_question=follow_up_question
        )
    
    async def _generate_follow_up_question(self, missing_fields: List[str]) -> Optional[str]:
        """Generate a follow-up question for missing profile information."""
        field_descriptions = {
            "training_history": "past workout experience",
            "fitness_background": "athletic background or sports history",
            "weekly_schedule": "availability for workouts during the week",
            "available_equipment": "equipment you have access to",
            "fitness_goals": "specific fitness goals you want to achieve",
            "health_constraints": "any injuries or health conditions to consider"
        }
        missing_descriptions = [field_descriptions.get(field, field) for field in missing_fields]
        prompt = f"""Based on the fitness profile information so far, I need to know about the user's {', '.join(missing_descriptions)}.
        Generate a single, conversational question to ask the user that would help me understand their {missing_descriptions[0]} better.
        Make it friendly and specific to fitness needs. Return ONLY the question text."""
        
        messages = [
            Message(role=Role.SYSTEM, content="You are a friendly fitness profile assistant"),
            Message(role=Role.USER, content=prompt)
        ]
        question = await self.llm.generate(messages)
        return question.strip().strip('"')
