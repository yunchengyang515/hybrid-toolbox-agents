# Profile Extraction Agent

## Overview

The Profile Extraction Agent collects and structures user fitness information through natural conversation. It's designed for hybrid fitness programs combining running and strength training.

## Key Features

- Extract structured fitness profile information from natural language
- Identify missing information and generate relevant follow-up questions
- Maintain conversation history to improve extraction quality
- Prioritize questions based on importance for hybrid training plans

## Flow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  User Input │────▶│  Extract    │────▶│  Response   │
│  (Initial)  │     │  Profile    │     │  with       │
└─────────────┘     └─────────────┘     │  Questions  │
                                       └──────┬──────┘
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  User Input │     │  Extract    │     │  Updated    │
│  (Answer)   │◀────│  with       │◀────│  History    │
└─────┬───────┘     │  History    │     └─────────────┘
      │             └─────────────┘
      ▼
┌─────────────┐
│  Complete   │
│  Profile    │
└─────────────┘
```

## API Endpoints

### Extract Profile

```
POST /extract
```

Extracts structured profile information from user input.

#### Example Usage

Start a conversation with initial user input:

```json
{
  "user_input": "I want to start a hybrid training program. I'm a runner who does 20 miles per week."
}
```

Response with missing information:

```json
{
  "profile_data": {
    "training_history": "Running 20 miles per week",
    "fitness_background": null,
    "weekly_schedule": null,
    "available_equipment": null,
    "training_goals": null,
    "health_constraints": null
  },
  "raw_input": "I want to start a hybrid training program. I'm a runner who does 20 miles per week.",
  "missing_fields": [
    "fitness_background",
    "weekly_schedule",
    "available_equipment",
    "training_goals",
    "health_constraints"
  ],
  "is_complete": false,
  "follow_up_questions": [
    "What specific fitness goals do you have for your hybrid training program?"
  ]
}
```

Continue the conversation by including history:

```json
{
  "user_input": "I want to get stronger while maintaining my running endurance. I'd like to run a half marathon next year.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I want to start a hybrid training program. I'm a runner who does 20 miles per week."
    },
    {
      "role": "assistant",
      "content": "What specific fitness goals do you have for your hybrid training program?"
    }
  ]
}
```

## Testing with Postman

### Setup

1. Create a new Postman collection named "Profile Extraction API"
2. Add a new request named "Extract Profile"
3. Set the HTTP method to POST
4. Set the request URL to `http://localhost:8000/profile/extract`
5. Set the Content-Type header to `application/json`

### Test Cases

#### Initial Profile Extraction

1. In the request body, enter:

```json
{
  "user_input": "Hi, I've been running for about 2 years, mostly 5K distances. I want to start adding some strength work."
}
```

2. Send the request
3. Save the response for the follow-up request

#### Follow-up Request

1. Create a new request named "Extract Profile - Follow Up"
2. In the request body, use the following template, replacing values from the previous response:

```json
{
  "user_input": "I want to improve my 5K time and build upper body strength. I'm free to train Monday, Wednesday, Friday, and weekends.",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hi, I've been running for about 2 years, mostly 5K distances. I want to start adding some strength work."
    },
    {
      "role": "assistant",
      "content": "What are your specific fitness goals with this hybrid training program?"
    }
  ]
}
```

3. Send the request

#### Using the Helper Method

To build the next conversation history properly:

1. Extract the follow-up question from the response: `response.follow_up_questions[0]`
2. Use the `build_next_conversation_history` method in your application:

```python
next_history = service.build_next_conversation_history(
    current_history,  # from previous request
    response,         # current response object
    follow_up_question  # from response.follow_up_questions[0]
)
```

3. Use this history in your next request

### Complete Conversation Flow Script

Here's a Python script to demonstrate the complete flow:

```python
import requests
import json

BASE_URL = "http://localhost:8000/profile"
service_url = f"{BASE_URL}/extract"

# Initial request
initial_input = {
    "user_input": "Hi, I've been running for about 2 years, mostly 5K distances. I want to start adding some strength work."
}

response = requests.post(service_url, json=initial_input)
result = response.json()

conversation_history = []
if not result["is_complete"] and result["follow_up_questions"]:
    # Add initial exchange to history
    conversation_history.append({"role": "user", "content": result["raw_input"]})
    conversation_history.append({"role": "assistant", "content": result["follow_up_questions"][0]})

    # Second exchange
    follow_up_response = {
        "user_input": "I want to improve my 5K time and build upper body strength.",
        "conversation_history": conversation_history
    }

    response = requests.post(service_url, json=follow_up_response)
    result = response.json()

    # Continue until profile is complete
    while not result["is_complete"] and result["follow_up_questions"]:
        # Update history
        conversation_history.append({"role": "user", "content": result["raw_input"]})
        conversation_history.append({"role": "assistant", "content": result["follow_up_questions"][0]})

        # Get user input (simulated here)
        next_input = "I have dumbbells at home and access to a gym. I can train 4 days a week."

        # Make next request
        follow_up_response = {
            "user_input": next_input,
            "conversation_history": conversation_history
        }

        response = requests.post(service_url, json=follow_up_response)
        result = response.json()

print("Final profile data:", json.dumps(result["profile_data"], indent=2))
```

## Client Implementation Tips

For frontend clients:

1. Start with an initial user input
2. Store the response and display follow-up questions
3. When user answers, include the complete conversation history in the next request
4. Maintain the conversation history by appending the new question and user's answer
5. Repeat until `is_complete` is true
