import json
import logging
from typing import List, Dict, Any, Optional, Union, Tuple

from common.llm import LLMClient
from common.schemas import Message, Role, TrainingPlan
from .schemas import (
    ProfileExtractRequest, 
    ProfileExtractResponse,
    GeneratePlanRequest, 
    GeneratePlanResponse
)
from .config import PlanningConfig

logger = logging.getLogger(__name__)

class PlanningService:
    """Service for hybrid training planning, including profile extraction and plan generation."""

    def __init__(self):
        self.config = PlanningConfig()
        self.llm = LLMClient()

    # Profile extraction methods (adapted from original ProfileExtractionService)
    async def extract_profile(self, request: ProfileExtractRequest) -> ProfileExtractResponse:
        """Extract profile data from user input and handle missing information."""
        # Get LLM response with profile data
        parsed_result = await self._extract_profile_data(request)
        
        # Process missing fields
        missing_fields = self._get_missing_fields(parsed_result)
        
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
        
    async def _extract_profile_data(self, request: ProfileExtractRequest) -> Dict[str, Any]:
        """Extract profile data using LLM."""
        messages = self._build_profile_messages(request)
        result = await self.llm.generate(messages)
        result = result.strip()

        # Validate JSON response
        try:
            parsed_result = json.loads(result)
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from LLM")
            parsed_result = {}
            
        # Remove missing_fields from the result if present
        if isinstance(parsed_result, dict) and "missing_fields" in parsed_result:
            parsed_result.pop("missing_fields", None)
            
        return parsed_result
    
    def _build_profile_messages(self, request: ProfileExtractRequest) -> List[Message]:
        """Build messages for LLM based on request and system prompt for profile extraction."""
        messages = [Message(role=Role.SYSTEM, content=self.config.profile_system_prompt)]
        
        if request.conversation_history:
            for msg in request.conversation_history:
                role = Role.USER if msg.get("role") == "user" else Role.ASSISTANT
                messages.append(Message(role=role, content=msg.get("content", "")))
                
        messages.append(Message(role=Role.USER, content=request.user_input))
        return messages
        
    def _get_missing_fields(self, profile_data: Dict[str, Any]) -> List[str]:
        """Determine which required fields are missing from the profile data."""
        missing_fields = []
        for field in self.config.required_fields:
            if field not in profile_data or not profile_data.get(field):
                missing_fields.append(field)
        return missing_fields

    def _prioritize_missing_fields(self, missing_fields: List[str]) -> List[str]:
        """Prioritize missing fields based on importance for hybrid training."""
        return sorted(missing_fields, key=lambda field: 
                     self.config.priority_order.index(field) 
                     if field in self.config.priority_order 
                     else len(self.config.priority_order))
    
    async def _generate_follow_up_question(self, missing_fields: List[str]) -> Optional[str]:
        """Generate a follow-up question for missing profile information."""
        if not missing_fields:
            return None
            
        missing_descriptions = [self.config.field_descriptions.get(field, field) for field in missing_fields]
        
        prompt = self.config.question_prompt_template.format(
            all_missing=', '.join(missing_descriptions),
            first_missing=missing_descriptions[0]
        )

        messages = [
            Message(role=Role.SYSTEM, content=self.config.question_system_prompt),
            Message(role=Role.USER, content=prompt)
        ]
        question = await self.llm.generate(messages)
        return question.strip().strip('"')

    # Plan generation methods
    async def generate_plan(self, request: GeneratePlanRequest) -> GeneratePlanResponse:
        """Generate a complete training plan based on user profile."""
        # For MVP, generate guidelines instead of detailed JSON
        training_plan, guidelines = await self._generate_plan_guidelines(request)
        
        profile_summary = {
            "goals": request.profile.get("training_goals"),
            "experience": request.profile.get("fitness_background"),
            "schedule": request.profile.get("weekly_schedule"),
            "constraints": request.profile.get("health_constraints")
        }
        
        return GeneratePlanResponse(
            plan=training_plan,
            profile_summary=profile_summary,
            recommendations=[],
            guidelines=guidelines
        )
    
    async def _generate_plan_guidelines(self, request: GeneratePlanRequest) -> Tuple[TrainingPlan, str]:
        """Generate conversational plan guidelines instead of detailed JSON."""
        # Build message for plan guidelines generation
        messages = self._build_plan_guidelines_messages(request)
        
        # Get response from LLM
        result = await self.llm.generate(messages)
        guidelines = result.strip()
        
        # Create a minimal plan structure for the response
        # In MVP, this will be mostly empty as we're focusing on the guidelines
        plan = TrainingPlan(
            title=f"{request.plan_parameters.duration_weeks}-Week Hybrid Training Plan",
            description=f"A {request.plan_parameters.emphasis} training program customized to your profile",
            weeks=[]
        )
        
        return plan, guidelines
    
    def _build_plan_guidelines_messages(self, request: GeneratePlanRequest) -> List[Message]:
        """Build messages for LLM to generate plan guidelines."""
        system_prompt = """You are an expert hybrid training coach writing directly to your client about their personalized training plan.
Speak as if you're having a one-on-one conversation with them.

DO NOT use meta-commentary like "Here's a conversational overview" or "This is your plan".
Instead, communicate directly: "I've created this 4-week plan for you based on your goals..."

Your response should:
- Use a warm, encouraging tone with "you" and "your" language
- Begin with a brief personalized greeting acknowledging their specific situation
- Explain the structure of their training weeks and progression
- Describe the weekly balance of running and strength sessions
- Address how you've adapted the plan for their specific goals and constraints
- Include any special modifications based on their health concerns
- End with an encouraging message about their fitness journey

Keep it concise, motivational, and free of technical jargon.
"""
        
        user_prompt = f"""Create a personalized training plan message for a client with this profile:

PROFILE:
- Training history: {request.profile.get('training_history', 'Not specified')}
- Fitness background: {request.profile.get('fitness_background', 'Not specified')}
- Weekly schedule: {request.profile.get('weekly_schedule', 'Not specified')}
- Available equipment: {request.profile.get('available_equipment', 'Not specified')}
- Training goals: {request.profile.get('training_goals', 'Not specified')}
- Health constraints: {request.profile.get('health_constraints', 'Not specified')}

PLAN PARAMETERS:
- Duration: {request.plan_parameters.duration_weeks} weeks
- Emphasis: {request.plan_parameters.emphasis}

Write directly to the client about their {request.plan_parameters.duration_weeks}-week plan as their personal coach.
"""
        
        return [
            Message(role=Role.SYSTEM, content=system_prompt),
            Message(role=Role.USER, content=user_prompt)
        ]
    
    def _build_plan_generation_messages(self, request: GeneratePlanRequest) -> List[Message]:
        """Build messages for LLM based on request and system prompt for plan generation."""
        # Create a prompt that includes the profile and plan parameters
        user_prompt = f"""Generate a hybrid training plan with the following information:

Profile:
- Training history: {request.profile.get('training_history', 'Not specified')}
- Fitness background: {request.profile.get('fitness_background', 'Not specified')}
- Weekly schedule: {request.profile.get('weekly_schedule', 'Not specified')}
- Available equipment: {request.profile.get('available_equipment', 'Not specified')}
- Training goals: {request.profile.get('training_goals', 'Not specified')}
- Health constraints: {request.profile.get('health_constraints', 'Not specified')}

Plan Parameters:
- Duration: {request.plan_parameters.duration_weeks} weeks
- Emphasis: {request.plan_parameters.emphasis}

Return the full training plan as JSON that follows the TrainingPlan schema.
"""
        messages = [
            Message(role=Role.SYSTEM, content=self.config.plan_generation_system_prompt),
            Message(role=Role.USER, content=user_prompt)
        ]
        return messages
        
    # Helper method for conversation history
    def build_next_conversation_history(
        self, 
        current_history: Optional[List[Dict[str, str]]], 
        response: ProfileExtractResponse,
        follow_up_question: str
    ) -> List[Dict[str, str]]:
        """Build conversation history for the next request."""
        # Initialize conversation history if None
        history = current_history or []
        # Add the original user message to history if not already there
        if not history or history[-1]["role"] != "user" or history[-1]["content"] != response.raw_input:
            history.append({"role": "user", "content": response.raw_input})
        # Add the system's follow-up question to history
        history.append({"role": "assistant", "content": follow_up_question})
        
        return history
