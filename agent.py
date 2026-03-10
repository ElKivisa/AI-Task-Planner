import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class PlanningAgent:
    def __init__(self, tasks):
        self.tasks = tasks
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrado en las variables de entorno.")
        
        self.client = genai.Client(api_key=api_key)

    def analyze_tasks(self):
        prompt = f"""
        Analiza las siguientes tareas y haz lo siguiente:
        1 -Determina una prioridad de las tareas
        2 -Genera un plan semanal simple
        3 -Explica brevemente el razonamiento

        Tareas:
        {self.tasks}

        Responde en este formato:

        Prioridad:
        1-
        2-
        3-

        Plan Semanal:
        Lunes:
        Martes:
        Miércoles:

        Razonamiento:
        """

        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text.strip()