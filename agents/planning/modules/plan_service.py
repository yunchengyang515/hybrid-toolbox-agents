import json
import logging
import io
import csv
from typing import List, Dict, Any, Optional, Tuple

from common.llm import LLMClient
from common.schemas import Message, Role, TrainingPlan
from ..schemas import GeneratePlanRequest, GeneratePlanResponse
from ..config import PlanningConfig

logger = logging.getLogger(__name__)

class PlanGenerationService:
    """Service for generating training plans based on user profiles."""

    def __init__(self, config: Optional[PlanningConfig] = None, llm: Optional[LLMClient] = None):
        self.config = config or PlanningConfig()
        self.llm = llm or LLMClient()

    async def generate_plan(self, request: GeneratePlanRequest) -> GeneratePlanResponse:
        """Generate a complete training plan based on user profile."""
        # Step 1: Always generate conversational guidelines first
        training_plan, guidelines = await self._generate_plan_guidelines(request)
        
        # Step 2: Check if we need to convert to other formats
        table_format = None
        csv_format = None
        
        # If format is specified as something other than guidelines
        if hasattr(request.plan_parameters, 'format') and request.plan_parameters.format != 'guidelines':
            # Convert guidelines to structured data
            structured_plan = await self._guidelines_to_structured_plan(guidelines, request)
            
            # Generate requested format
            if request.plan_parameters.format == 'table':
                table_format = self._structured_to_table(structured_plan)
            elif request.plan_parameters.format == 'csv':
                csv_format = self._structured_to_csv(structured_plan)
        
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
            guidelines=guidelines,
            table_format=table_format,
            csv_format=csv_format
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
    
    async def _guidelines_to_structured_plan(self, guidelines: str, request: GeneratePlanRequest) -> List[Dict[str, Any]]:
        """Convert conversational guidelines to a structured plan format."""
        system_prompt = """You are an expert at converting conversational training plan guidelines into structured data.
Given a conversational training plan, extract a structured weekly schedule.
Return a valid JSON array of weekly plans where each week contains an array of daily workouts.

Format your response as a valid JSON array with this structure:
[
  {
    "week": 1,
    "days": [
      {
        "day": "Monday",
        "workout_type": "Strength",
        "details": "Upper body focus: 3 sets of 8-10 reps"
      },
      {
        "day": "Tuesday", 
        "workout_type": "Run", 
        "details": "Easy 5km run"
      },
      ...
    ]
  },
  ...
]

DO NOT include any explanatory text or markdown formatting. ONLY return the valid JSON array.
"""
        
        user_prompt = f"""Extract the structured workout schedule from these training plan guidelines:

{guidelines}

The plan is {request.plan_parameters.duration_weeks} weeks long with a {request.plan_parameters.emphasis} emphasis.
Parse out each week's activities into a structured JSON format that shows each day's workout type and details.
"""
        
        messages = [
            Message(role=Role.SYSTEM, content=system_prompt),
            Message(role=Role.USER, content=user_prompt)
        ]
        
        result = await self.llm.generate(messages)
        result = result.strip()
        
        # Clean up the result to handle potential markdown code blocks
        if result.startswith("```"):
            result = result.strip("```")
        
        try:
            structured_plan = json.loads(result)
        except json.JSONDecodeError:
            logger.error("Invalid JSON response for structured plan")
            structured_plan = []
        
        return structured_plan
    
    def _structured_to_table(self, structured_plan: List[Dict[str, Any]]) -> str:
        """Convert structured plan to a table format."""
        table = io.StringIO()
        writer = csv.writer(table, delimiter='\t')
        
        # Write headers
        writer.writerow(["Week", "Day", "Workout Type", "Details"])
        
        # Write rows
        for week in structured_plan:
            for day in week.get("days", []):
                writer.writerow([week.get("week"), day.get("day"), day.get("workout_type"), day.get("details")])
        
        return table.getvalue()
    
    def _structured_to_csv(self, structured_plan: List[Dict[str, Any]]) -> str:
        """Convert structured plan to CSV format."""
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        
        # Write headers
        writer.writerow(["Week", "Day", "Workout Type", "Details"])
        
        # Write rows
        for week in structured_plan:
            for day in week.get("days", []):
                writer.writerow([week.get("week"), day.get("day"), day.get("workout_type"), day.get("details")])
        
        return csv_file.getvalue()
    
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
