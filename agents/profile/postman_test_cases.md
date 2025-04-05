# Profile Agent Postman Test Cases

This document provides JSON request bodies for testing the Profile Extraction Agent with Postman, covering various conversation flows.

## Test Flow 1: Runner Looking to Add Strength Training

### Initial Request

```json
{
  "user_input": "I'm a runner looking to add strength training. I typically run about 50 km per week and have completed a few half marathons."
}
```

### Follow-up 1 (Assuming first response asks about goals)

```json
{
  "user_input": "I want to improve my running economy and prevent injuries. I'd like to maintain my endurance while building some muscle.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I'm a runner looking to add strength training. I typically run about 50 km per week and have completed a few half marathons."
    },
    {
      "role": "assistant",
      "content": "What are your specific fitness goals for adding strength training to your running routine?"
    }
  ]
}
```

### Follow-up 2 (Schedule information)

```json
{
  "user_input": "I can train Monday through Friday in the mornings before work, and I have longer sessions available on weekends.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I'm a runner looking to add strength training. I typically run about 25 miles per week and have completed a few half marathons."
    },
    {
      "role": "assistant",
      "content": "What are your specific fitness goals for adding strength training to your running routine?"
    },
    {
      "role": "user",
      "content": "I want to improve my running economy and prevent injuries. I'd like to maintain my endurance while building some muscle."
    },
    {
      "role": "assistant",
      "content": "What does your weekly schedule look like for training? When are you available to work out?"
    }
  ]
}
```

### Follow-up 3 (Equipment information)

```json
{
  "user_input": "I have a gym membership and some basic equipment at home - dumbbells, kettlebells, and resistance bands.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I'm a runner looking to add strength training. I typically run about 25 miles per week and have completed a few half marathons."
    },
    {
      "role": "assistant",
      "content": "What are your specific fitness goals for adding strength training to your running routine?"
    },
    {
      "role": "user",
      "content": "I want to improve my running economy and prevent injuries. I'd like to maintain my endurance while building some muscle."
    },
    {
      "role": "assistant",
      "content": "What does your weekly schedule look like for training? When are you available to work out?"
    },
    {
      "role": "user",
      "content": "I can train Monday through Friday in the mornings before work, and I have longer sessions available on weekends."
    },
    {
      "role": "assistant",
      "content": "What equipment do you have access to for your strength training?"
    }
  ]
}
```

## Test Flow 2: Complete Information in Initial Request

### Initial Request with Complete Information

```json
{
  "user_input": "I'm looking to start a hybrid training program. My background is mostly bodybuilding with 5 years of experience, but I've recently started running 10K distances. My goal is to maintain my muscle mass while improving my 10K time. I have access to a full gym and can train 4 days per week - Monday, Tuesday, Thursday, and Saturday. I have no major health issues but sometimes experience knee pain after long runs."
}
```

## Test Flow 3: Weight Loss Focus

### Initial Request

```json
{
  "user_input": "I need to lose about 30 pounds and improve my overall fitness. I haven't exercised much in recent years."
}
```

### Follow-up 1 (Training History)

```json
{
  "user_input": "I played basketball in high school but that was 10 years ago. Since then, I've been mostly sedentary except for occasional walks.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I need to lose about 30 pounds and improve my overall fitness. I haven't exercised much in recent years."
    },
    {
      "role": "assistant",
      "content": "Can you tell me more about your fitness background or any past exercise experience you've had?"
    }
  ]
}
```

### Follow-up 2 (Equipment/Access)

```json
{
  "user_input": "I don't have a gym membership yet but I'm willing to get one. At home I just have a yoga mat and some resistance bands.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I need to lose about 30 pounds and improve my overall fitness. I haven't exercised much in recent years."
    },
    {
      "role": "assistant",
      "content": "Can you tell me more about your fitness background or any past exercise experience you've had?"
    },
    {
      "role": "user",
      "content": "I played basketball in high school but that was 10 years ago. Since then, I've been mostly sedentary except for occasional walks."
    },
    {
      "role": "assistant",
      "content": "What equipment do you have access to for your workouts? Do you have a gym membership or any home equipment?"
    }
  ]
}
```

### Follow-up 3 (Schedule)

```json
{
  "user_input": "I can work out after work on weekdays (around 6pm) and anytime on weekends. I'd like to start with 3-4 days per week.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I need to lose about 30 pounds and improve my overall fitness. I haven't exercised much in recent years."
    },
    {
      "role": "assistant",
      "content": "Can you tell me more about your fitness background or any past exercise experience you've had?"
    },
    {
      "role": "user",
      "content": "I played basketball in high school but that was 10 years ago. Since then, I've been mostly sedentary except for occasional walks."
    },
    {
      "role": "assistant",
      "content": "What equipment do you have access to for your workouts? Do you have a gym membership or any home equipment?"
    },
    {
      "role": "user",
      "content": "I don't have a gym membership yet but I'm willing to get one. At home I just have a yoga mat and some resistance bands."
    },
    {
      "role": "assistant",
      "content": "What does your weekly schedule look like? When would you be available to train during the week?"
    }
  ]
}
```

## Test Flow 4: Testing Health Constraints

### Initial Request

```json
{
  "user_input": "I want to get fit but I have lower back pain and asthma."
}
```

### Follow-up 1 (Goals)

```json
{
  "user_input": "I'd like to strengthen my core to help with my back pain, improve my cardiovascular health, and maybe lose a bit of weight.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I want to get fit but I have lower back pain and asthma."
    },
    {
      "role": "assistant",
      "content": "What specific fitness goals would you like to achieve with your hybrid training program?"
    }
  ]
}
```

### Follow-up 2 (Training History)

```json
{
  "user_input": "I've tried yoga and swimming in the past. Swimming seemed to work well with my asthma. I've never really done any strength training before.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I want to get fit but I have lower back pain and asthma."
    },
    {
      "role": "assistant",
      "content": "What specific fitness goals would you like to achieve with your hybrid training program?"
    },
    {
      "role": "user",
      "content": "I'd like to strengthen my core to help with my back pain, improve my cardiovascular health, and maybe lose a bit of weight."
    },
    {
      "role": "assistant",
      "content": "Can you tell me about your past workout experience or training history?"
    }
  ]
}
```

## Test Flow 5: Advanced Athlete Needing Specialized Plan

### Initial Request

```json
{
  "user_input": "I'm training for a triathlon in 6 months. Currently swimming 2x a week, biking 3x a week, and running 3x a week."
}
```

### Follow-up 1 (Schedule and equipment)

```json
{
  "user_input": "I train every day with Monday as a recovery day. I have access to a full gym, a pool, my road bike, and all the standard triathlon gear. I typically train early mornings on weekdays and do longer sessions on weekends.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I'm training for a triathlon in 6 months. Currently swimming 2x a week, biking 3x a week, and running 3x a week."
    },
    {
      "role": "assistant",
      "content": "What's your weekly training schedule like and what equipment do you have access to for your workouts?"
    }
  ]
}
```

### Follow-up 2 (Background)

```json
{
  "user_input": "I was a competitive swimmer in college. I've completed two Olympic distance triathlons before but this will be my first half-Ironman distance. I'm strong in swimming, decent in cycling, but running is my weakness.",
  "conversation_history": [
    {
      "role": "user",
      "content": "I'm training for a triathlon in 6 months. Currently swimming 2x a week, biking 3x a week, and running 3x a week."
    },
    {
      "role": "assistant",
      "content": "What's your weekly training schedule like and what equipment do you have access to for your workouts?"
    },
    {
      "role": "user",
      "content": "I train every day with Monday as a recovery day. I have access to a full gym, a pool, my road bike, and all the standard triathlon gear. I typically train early mornings on weekdays and do longer sessions on weekends."
    },
    {
      "role": "assistant",
      "content": "Can you tell me about your athletic background and previous experience with triathlons or endurance events?"
    }
  ]
}
```

## Using These Test Cases

1. Create a new request in Postman
2. Set the method to POST and URL to `http://localhost:8000/profile/extract`
3. Add header `Content-Type: application/json`
4. Copy the JSON request body from the test case you want to try
5. Send the request and examine the response
6. For follow-up requests, copy the next test case in the flow

These test cases cover diverse scenarios to test the profile extraction agent's ability to handle different user backgrounds, goals, and conversation patterns.
