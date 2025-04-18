# Hybrid Training Planning Agent

## Overview

The Planning Agent is an all-in-one solution for creating personalized hybrid training plans that combine running and strength training. It collects user information, designs appropriate training blocks, and organizes them into comprehensive weekly plans.

## Key Components

1. **Profile Extraction**

   - Extracts structured fitness profile data from natural language input
   - Identifies missing information and generates relevant follow-up questions
   - Maintains conversation history to improve extraction quality
   - Prioritizes questions based on importance for hybrid training plans

2. **Plan Generation**

   - Creates complete training plans based on user profiles
   - Balances running and strength training components
   - Customizes plans according to specified parameters (duration, emphasis, etc.)
   - Provides supplementary recommendations

3. **Plan Adjustment**
   - Modifies existing plans based on user feedback
   - Preserves the plan's core structure while addressing specific concerns
   - Summarizes the changes made and their rationale
   - Offers additional recommendations for optimal results

## API Endpoints

### 1. Extract Profile
