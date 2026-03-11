import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class PlanningAgent:

    #Constructor del agente, obtiene la clave de la API del .env
    def __init__(self, tasks):
        self.tasks = tasks

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        self.client = genai.Client(api_key=api_key)

    #Función para analizar las tareas, generar un plan semanal y explicar el razonamiento
    def analyze_tasks(self):

        prompt = f"""
You are a task planning agent.

Analyze the following list of tasks and do the following:

1. Determine the priority order of the tasks
2. Generate a simple weekly plan
3. Explain briefly the reasoning

Task list:
{self.tasks}

Respond in English using this exact format, adding more rows if necessary:

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

        #Genera la respuesta utilizando el modelo de lenguaje de Gemini
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text.strip()