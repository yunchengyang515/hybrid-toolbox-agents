import json
import logging
from typing import List, Dict, Any, Optional

from common.llm import LLMClient
from common.schemas import Message, Role
from ..schemas import ProfileExtractRequest, ProfileExtractResponse
from ..config import PlanningConfig

logger = logging.getLogger(__name__)

class ProfileExtractionService:
    """Service for extracting user profile information from natural language inputs."""

    def __init__(self, config: Optional[PlanningConfig] = None, llm: Optional[LLMClient] = None):
        self.config = config or PlanningConfig()
        self.llm = llm or LLMClient()

    async def extract_profile(self, request: ProfileExtractRequest) -> ProfileExtractResponse:
        """Extract profile data from user input and handle missing information."""
        # Get LLM response with profile data
        parsed_result = await self._extract_profile_data(request)
        
        # Process missing fields
        missing_fields = self._get_missing_fields(parsed_result)
        
        # Check if profile is complete
        is_complete = len(missing_fields) == 0
        print(f"missing fields: {missing_fields}")

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
            logger.warning(f"Invalid JSON response from LLM. Attempting to repair...")
            
            # Try to repair the JSON
            try:
                repaired_json = await self._repair_json(result)
                if repaired_json:
                    parsed_result = repaired_json
                else:
                    logger.error("Could not repair JSON - repair failed")
                    parsed_result = {}
            except Exception as e:
                logger.error(f"Error during JSON repair: {str(e)}")
                parsed_result = {}
            
        # Remove missing_fields from the result if present
        if isinstance(parsed_result, dict) and "missing_fields" in parsed_result:
            parsed_result.pop("missing_fields", None)
            
        return parsed_result
    
    async def _repair_json(self, malformed_json: str) -> Optional[Dict[str, Any]]:
        """Attempt to repair malformed JSON by asking the LLM to fix it."""
        try:
            # Prepare prompt for JSON repair
            repair_prompt = self.config.json_repair_prompt.format(json_content=malformed_json)
            
            # Send the repair request to the LLM
            messages = [Message(role=Role.USER, content=repair_prompt)]
            repaired_text = await self.llm.generate(messages)
            repaired_text = repaired_text.strip()
            
            # Try to parse the repaired JSON
            repaired_json = json.loads(repaired_text)
            logger.info("Successfully repaired JSON")
            return repaired_json
        
        except json.JSONDecodeError:
            logger.error("JSON repair attempt failed - still invalid JSON")
            return None
        except Exception as e:
            logger.error(f"Error during JSON repair attempt: {str(e)}")
            return None
    
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
            # Check if field is missing, empty, or contains placeholder text
            value = profile_data.get(field)
            
            if (
                field not in profile_data or 
                not value or 
                value == "" or 
                value == "null" or
                value is None or
                isinstance(value, str) and any(placeholder in value.lower() for placeholder in [
                    "no mention", 
                    "not specified", 
                    "not mentioned", 
                    "not provided", 
                    "unknown", 
                    "unclear",
                    "not stated",
                    "not indicated"
                ])
            ):
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
