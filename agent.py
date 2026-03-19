import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

class PlanningAgent:
    def __init__(self, tasks):
        self.tasks = tasks

        # Modelo (LLM)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

        # Prompt template
        self.prompt = PromptTemplate(
            input_variables=["tasks"],
            template="""
You are an AI planning assistant.

Your job is to:
1. Analyze the tasks
2. Prioritize them
3. Create a weekly plan
4. Explain your reasoning

Tasks:
{tasks}

Respond EXACTLY in this format:

Priority:
1.
2.
3.

Weekly plan:
Monday:
Tuesday:
Wednesday:
Thursday:
Friday:
Saturday:
Sunday:

Reason:
"""
        )

    def analyze_tasks(self):
        try:
            # Crear el prompt final
            formatted_prompt = self.prompt.format(tasks=self.tasks)

            # Llamar al modelo
            response = self.llm.invoke(formatted_prompt)

            return response.content

        except Exception as e:
            return f"Error: {e}"