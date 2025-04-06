class ProfileConfig:
    """Configuration for profile extraction."""
    
    def __init__(self):
        # Required fields for a complete user profile
        self.required_fields = [
            "training_history", 
            "fitness_background", 
            "weekly_schedule", 
            "available_equipment",
            "training_goals",
            "health_constraints"
        ]
        
        # Priority order for asking about missing fields
        self.priority_order = [
            "training_goals",
            "training_history", 
            "weekly_schedule",
            "available_equipment",
            "fitness_background",
            "health_constraints"
        ]
        
        # Descriptions for each field to use in follow-up questions
        self.field_descriptions = {
            "training_history": "past workout experience (e.g., running, lifting, or hybrid)",
            "fitness_background": "athletic background or sports history",
            "weekly_schedule": "availability for training during the week",
            "available_equipment": "equipment available for workouts (e.g., kettlebells, gym access)",
            "training_goals": "specific goals like building strength or improving running performance",
            "health_constraints": "any injuries, medical conditions, or recovery concerns"
        }
        
        # System prompt for profile extraction
        self.system_prompt = """You are an AI fitness assistant focused on building hybrid training plans that combine running and strength training. 
Your job is to extract structured user profile information from natural language inputs to support personalized plan generation.
Make sure ONLY json is returned, with no additional text or explanations. As it will be parsed by a system,

Extract and return the following fields:
- training_history (e.g., experience with running, lifting, or hybrid workouts)
- fitness_background (e.g., athletic history, sports played, training style)
- weekly_schedule (days and times available for training)
- available_equipment (e.g., kettlebells, barbell, gym access, treadmill)
- training_goals (e.g., run a sub-20 5K, build strength, lose fat)
- health_constraints (e.g., injuries, conditions, recovery needs)

ONLY Return a JSON object with these fields, plus a "missing_fields" array listing any fields that are unclear or missing.
Use a hybrid training lens—if a user mentions only running or only lifting, consider the other as potentially missing unless clearly ruled out.
"""

        # System prompt for generating follow-up questions
        self.question_system_prompt = "You are a friendly fitness profile assistant"
        
        # Template for generating follow-up question prompts
        self.question_prompt_template = """I'm helping create a hybrid training plan that combines running and strength work. 
So far, I still need to know more about the user's {all_missing}.
Generate a friendly, natural follow-up question that asks specifically about their {first_missing} in the context of hybrid training.
Be concise and helpful. Return ONLY the question text."""
