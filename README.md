# Hybrid Toolbox Agents API

Multi-endpoint agent system for hybrid training plan generation, built with FastAPI and Groq LLM.

## Overview

This API provides a comprehensive planning agent for creating hybrid training plans that combine running and strength training:

- **Planning Agent**: Extracts user profiles, designs training blocks, and organizes them into comprehensive weekly plans
  - Profile Extraction: Collects and structures user fitness information
  - Training Design: Creates appropriate training blocks based on user profiles
  - Plan Organization: Schedules training blocks into a cohesive weekly plan

## Setup Instructions

### Prerequisites

- Python 3.10+
- Groq API key

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd hybrid-toolbox-agents
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment variables file:

```bash
cp .env.example .env
```

5. Edit `.env` and add your API keys

## Local Development

### Starting the FastAPI Server

To run the API server locally:

```bash
# Option 1: Using the main.py directly with auto-reload
python main.py

# Option 2: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

### API Documentation

FastAPI automatically generates interactive documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Health Check

Verify the server is running correctly:

```bash
curl http://localhost:8000/health
```

### Development Tools

- **Testing API Endpoints**: Use the Postman collection in `agents/planning/postman/` for testing endpoints
- **Code Formatting**: Run `black .` to format Python code
- **Linting**: Run `flake8 .` to check for code quality issues

## API Endpoints

### Planning Agent

- **POST /v1/planning/extract-profile**: Extracts user profile information from conversation
- **POST /v1/planning/generate-plan**: Generates a complete training plan based on user profile
- **POST /v1/planning/adjust-plan**: Adjusts an existing plan based on user feedback
