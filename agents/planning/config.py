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
            "health_constraints",
            "event_targets",
            "movement_limitations",
            "preferred_training_style"
        ]

        self.priority_order = [
            "training_goals",
            "training_history", 
            "weekly_schedule",
            "available_equipment",
            "fitness_background",
            "event_targets",
            "movement_limitations",
            "preferred_training_style",
            "health_constraints"
        ]

        self.field_descriptions = {
            "training_history": "past workout experience (e.g., running, lifting, hybrid sessions, CrossFit)",
            "fitness_background": "athletic background or sports history (e.g., former athlete, sedentary, gym-goer)",
            "weekly_schedule": "availability for training during the week (days, time windows)",
            "available_equipment": "equipment user can train with (e.g., barbell, kettlebells, sled, rower, treadmill)",
            "training_goals": "specific goals (e.g., build strength, run sub-20 5K, complete Hyrox)",
            "health_constraints": "injuries or medical limitations (e.g., recent surgery, joint pain)",
            "event_targets": "specific competition or event user is preparing for (e.g., Hyrox race, Spartan, 5K)",
            "movement_limitations": "non-medical limitations to movement (e.g., can’t squat below parallel, overhead pain)",
            "preferred_training_style": "if known, describe preferred training format (e.g., circuits, intervals, long runs)"
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
- health_constraints (e.g., injuries, conditions, recovery needs) - for this field, if user stated they don't have any health constraints, set it as "user stated they don't have any health constraints"



IMPORTANT:
- If information for a field is not included in user message or answers, set it to an empty string "" or null - DO NOT add text like "no mention" or "not specified"
- Only include information that is explicitly mentioned in the user input
- If user stated they don't have goal, history, equipment, or heath constraints / injuries, then you can format user's answer like "user stated they don't have any goal"/"user stated they don't have any history"/"user stated they don't have any equipment"/"user stated they don't have any health constraints"
- If the answers are vague or unclear, use the following guidelines:
- You can state that "user provided an unclear answer, we will use a generic setting" 
- Include the field in missing_fields array if information is not provided

CLARIFYING THE DIFFERENCE:
- `training_goals` = Desired capacities (e.g., "run sub-20 5K", "build strength", "improve engine", "maintain muscle while running more")
- `event_targets` = Specific event or race (e.g., "Hyrox Munich on July 6", "Spartan Super race", "5K Turkey Trot in November")

⚠️ SPECIAL NOTES ON HYBRID TRAINING:
- If user only mentions running goals, but has a background in lifting (or vice versa), still include BOTH under `training_goals` if implied. Example:
  > “I want to run a sub-20 5K” + “I lift 4x/week” → training_goals should include “run a sub-20 5K” AND “maintain strength”
- If user mentions Hyrox, assume goal includes **race readiness across all 8 functional stations + running**.
- If user says “I want to run a 5K at Hyrox”, correct that in your interpretation—there’s no 5K race at Hyrox.
- Use domain knowledge to separate aerobic vs strength demands, and preserve hybrid intent.


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




