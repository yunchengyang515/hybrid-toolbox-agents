# Hybrid Toolbox Agents API

Multi-endpoint agent system for hybrid training plan generation, built with FastAPI and Groq LLM.

## Overview

This API provides multiple specialized agents for creating comprehensive hybrid training plans:

- **Profile Agent**: Extracts and validates user fitness profiles
- **Designer Agent**: Creates training blocks based on user profiles
- **Planning Agent**: Organizes training blocks into comprehensive weekly plans
- **Feedback Agent**: Analyzes user feedback and suggests plan adjustments

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
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment variables file:

```bash
cp .env.example .env
```

5. Edit `.env` and add your API keys:

## API Endpoints

### Profile Agent

- **POST /profile**: Extracts and validates user fitness profiles

### Designer Agent

- **POST /designer**: Creates training blocks based on user profiles

### Planning Agent

- **POST /planning**: Organizes training blocks into comprehensive weekly plans

### Feedback Agent

- **POST /feedback**: Analyzes user feedback and suggests plan adjustments
