import json
import logging
from typing import List, Dict, Any, Optional

from common.llm import LLMClient
from common.schemas import Message, Role
from .schemas import ProfileExtractRequest, ProfileExtractResponse

logger = logging.getLogger(__name__)

class ProfileExtractionService:
    """Service for extracting user profile information for hybrid training."""

    def __init__(self):
        self.required_fields = [
            "training_history", 
            "fitness_background", 
            "weekly_schedule", 
            "available_equipment",
            "training_goals",
            "health_constraints"
        ]
        self.llm = LLMClient()

    async def extract_profile(self, request: ProfileExtractRequest) -> ProfileExtractResponse:
        """Extract profile data from user input and handle missing information."""
        # Prepare messages for LLM
        system_prompt = """You are an AI fitness assistant focused on building hybrid training plans that combine running and strength training. 
Your job is to extract structured user profile information from natural language inputs to support personalized plan generation.

Extract and return the following fields:
- training_history (e.g., experience with running, lifting, or hybrid workouts)
- fitness_background (e.g., athletic history, sports played, training style)
- weekly_schedule (days and times available for training)
- available_equipment (e.g., kettlebells, barbell, gym access, treadmill)
- training_goals (e.g., run a sub-20 5K, build strength, lose fat)
- health_constraints (e.g., injuries, conditions, recovery needs)

Return a JSON object with these fields, plus a "missing_fields" array listing any fields that are unclear or missing.
Use a hybrid training lens—if a user mentions only running or only lifting, consider the other as potentially missing unless clearly ruled out.
"""

        # Build conversation history
        messages = [Message(role=Role.SYSTEM, content=system_prompt)]
        if request.conversation_history:
            for msg in request.conversation_history:
                role = Role.USER if msg.get("role") == "user" else Role.ASSISTANT
                messages.append(Message(role=role, content=msg.get("content", "")))
        messages.append(Message(role=Role.USER, content=request.user_input))
        print(f"Messages: {messages}")
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

        # Generate follow-up questions if needed
        follow_up_questions = []
        if not is_complete:
            # Prioritize which missing field to ask about first
            prioritized_fields = self._prioritize_missing_fields(missing_fields)
            # Generate one follow-up question for the highest priority missing field
            follow_up_question = await self._generate_follow_up_question(prioritized_fields[:1])
            if follow_up_question:
                follow_up_questions.append(follow_up_question)

        return ProfileExtractResponse(
            profile_data=parsed_result,
            raw_input=request.user_input,
            missing_fields=missing_fields,
            is_complete=is_complete,
            follow_up_questions=follow_up_questions
        )

    def _prioritize_missing_fields(self, missing_fields: List[str]) -> List[str]:
        """Prioritize missing fields based on importance for hybrid training."""
        # Define priority order for fields (most important first)
        priority_order = [
            "training_goals",
            "training_history", 
            "weekly_schedule",
            "available_equipment",
            "fitness_background",
            "health_constraints"
        ]
        
        # Sort missing fields by priority
        return sorted(missing_fields, key=lambda field: 
                     priority_order.index(field) if field in priority_order else len(priority_order))
    
    async def _generate_follow_up_question(self, missing_fields: List[str]) -> Optional[str]:
        """Generate a follow-up question for missing profile information."""
        field_descriptions = {
            "training_history": "past workout experience (e.g., running, lifting, or hybrid)",
            "fitness_background": "athletic background or sports history",
            "weekly_schedule": "availability for training during the week",
            "available_equipment": "equipment available for workouts (e.g., kettlebells, gym access)",
            "training_goals": "specific goals like building strength or improving running performance",
            "health_constraints": "any injuries, medical conditions, or recovery concerns"
        }
        missing_descriptions = [field_descriptions.get(field, field) for field in missing_fields]
        prompt = f"""I'm helping create a hybrid training plan that combines running and strength work. 
So far, I still need to know more about the user's {', '.join(missing_descriptions)}.
Generate a friendly, natural follow-up question that asks specifically about their {missing_descriptions[0]} in the context of hybrid training.
Be concise and helpful. Return ONLY the question text."""

        messages = [
            Message(role=Role.SYSTEM, content="You are a friendly fitness profile assistant"),
            Message(role=Role.USER, content=prompt)
        ]
        question = await self.llm.generate(messages)
        return question.strip().strip('"')

    def build_next_conversation_history(
        self, 
        current_history: Optional[List[Dict[str, str]]], 
        response: ProfileExtractResponse,
        follow_up_question: str
    ) -> List[Dict[str, str]]:
        """
        Helper method to build the conversation history for the next request.
        
        Args:
            current_history: The current conversation history
            response: The current response object
            follow_up_question: The follow-up question that was asked
            
        Returns:
            Updated conversation history for the next request
        """
        # Initialize conversation history if None
        history = current_history or []
        
        # Add the original user message to history if not already there
        if not history or history[-1]["role"] != "user" or history[-1]["content"] != response.raw_input:
            history.append({"role": "user", "content": response.raw_input})
        
        # Add the system's follow-up question to history
        history.append({"role": "assistant", "content": follow_up_question})
        
        return history
