from tasks import tasks
from agent import PlanningAgent

def save_result(text):
    with open("plan_semanal.txt", "w", encoding="utf-8") as f:
        f.write(text)

def main():
    agent = PlanningAgent(tasks)
    result = agent.analyze_tasks()

    save_result(result)

if __name__ == "__main__":
    main()