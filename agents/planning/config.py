class PlanningConfig:
    """Configuration for the planning service."""
    
    def __init__(self):
        # Profile extraction configuration (moved from ProfileConfig)
        self.required_fields = [
            "training_history", 
            "fitness_background", 
            "weekly_schedule", 
            "available_equipment",
            "training_goals",
            "health_constraints"
        ]
        
        self.priority_order = [
            "training_goals",
            "training_history", 
            "weekly_schedule",
            "available_equipment",
            "fitness_background",
            "health_constraints"
        ]
        
        self.field_descriptions = {
            "training_history": "past workout experience (e.g., running, lifting, or hybrid)",
            "fitness_background": "athletic background or sports history",
            "weekly_schedule": "availability for training during the week",
            "available_equipment": "equipment available for workouts (e.g., kettlebells, gym access)",
            "training_goals": "specific goals like building strength or improving running performance",
            "health_constraints": "any injuries, medical conditions, or recovery concerns"
        }
        
        # System prompts for different functions
        
        # Profile extraction prompts
        self.profile_system_prompt = """You are an AI fitness assistant focused on building hybrid training plans that combine running and strength training. 
Your job is to extract structured user profile information from natural language inputs to support personalized plan generation.
Make sure ONLY json is returned, with no additional text or explanations. As it will be parsed by a system,

Extract and return the following fields:
- training_history (e.g., experience with running, lifting, or hybrid workouts)
- fitness_background (e.g., athletic history, sports played, training style)
- weekly_schedule (days and times available for training)
- available_equipment (e.g., kettlebells, barbell, gym access, treadmill)
- training_goals (e.g., run a sub-20 5K, build strength, Hyrox event)
- health_constraints (e.g., injuries, conditions, recovery needs)

ONLY Return a JSON object with these fields, plus a "missing_fields" array listing any fields that are unclear or missing.
Use a hybrid training lens—if a user mentions only running or only lifting, consider the other as potentially missing unless clearly ruled out.
"""

        self.question_system_prompt = "You are a friendly fitness profile assistant"
        
        self.question_prompt_template = """I'm helping create a hybrid training plan that combines running and strength work. 
So far, I still need to know more about the user's {all_missing}.
Generate a friendly, natural follow-up question that asks specifically about their {first_missing} in the context of hybrid training.
Be concise and helpful. Return ONLY the question text."""

        # Plan generation prompts
        self.plan_generation_system_prompt = """You are an expert hybrid training coach who specializes in combining running and strength training.
You create personalized training plans based on users' fitness profiles and goals.
Your plans should be detailed, including specific exercises, sets, reps, and rest periods.
Always focus on creating a balanced hybrid program that addresses both running and strength components.
Return ONLY valid JSON conforming to the TrainingPlan schema with no additional text or explanations.

The TrainingPlan schema includes:
- title: string - Overall name of the plan
- description: string - Brief summary of the plan's focus and approach
- weeks: array of TrainingWeek objects containing:
  - week_number: integer - Sequential week number
  - days: array of TrainingDay objects containing:
    - day: string - Name of day (e.g., "Monday", "Tuesday")
    - blocks: array of TrainingBlock objects containing:
      - name: string - Name of training block (e.g., "Morning Run", "Strength Circuit")
      - description: string - Brief description of the block's focus
      - exercises: array of Exercise objects containing:
        - name: string - Exercise name
        - sets: integer - Number of sets (optional)
        - reps: string - Repetition scheme (optional)
        - weight: string - Weight prescription (optional)
        - rest_seconds: integer - Rest between sets in seconds (optional)
        - notes: string - Additional instructions (optional)
- notes: string - Overall plan notes (optional)
"""

        self.recommendations_system_prompt = """You are an expert hybrid training coach providing targeted recommendations.
Based on user profiles and training plans, give specific, actionable recommendations.
Focus on practical advice that will help users succeed with their hybrid training program.
Keep recommendations concise, clear, and directly relevant to the user's specific situation.
"""



