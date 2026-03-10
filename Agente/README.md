# AI Task Planner

A small Python agent that uses an AI model to analyze tasks, prioritize them, and generate a simple weekly plan.

## Project files

- `main.py` → runs the program and saves the result
- `agent.py` → contains the AI planning agent
- `tasks.py` → contains the input tasks

## Requirements

Python 3.9+

Install dependencies:

pip install google-genai python-dotenv

## Configuration

Create a `.env` file in the project root and add your API key:

GEMINI_API_KEY=your_api_key

## Run the program

python main.py

## Output

The generated plan will be saved in:

plan_semanal.txt