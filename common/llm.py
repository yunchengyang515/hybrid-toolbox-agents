import groq
import logging
from typing import List, Dict, Any, Optional
from .config import settings
from .schemas import Message

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the Groq LLM client.
        
        Args:
            api_key: Optional Groq API key (defaults to env var)
            model: Model to use for completion (defaults to env var)
        """
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        self.client = groq.Client(api_key=self.api_key)
        
    async def generate(
        self, 
        messages: List[Message],
        temperature: float = None,
        max_tokens: int = None,
    ) -> str:
        """Generate a response from the LLM.
        
        Args:
            messages: List of Message objects
            temperature: Optional temperature parameter
            max_tokens: Optional max_tokens parameter
            
        Returns:
            str: The generated text
        """
        if not self.api_key:
            logger.error("Groq API key not provided")
            raise ValueError("Groq API key not provided")
            
        # Convert internal Message objects to dict format expected by Groq
        groq_messages = [{"role": m.role, "content": m.content} for m in messages]
        
        try:
            logger.info(f"Calling Groq with model {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=groq_messages,
                temperature=temperature or settings.DEFAULT_TEMPERATURE,
                max_tokens=max_tokens or settings.DEFAULT_MAX_TOKENS,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            raise
