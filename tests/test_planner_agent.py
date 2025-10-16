import sys
import os

# Get the path of the project root (one level up from 'target_folder')
# This line can be tricky, adjust based on your exact hierarchy
# The goal is to add the 'my_project' directory to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Now the absolute import will work
from agents.planner_agent import PlannerAgent

if __name__ == "__main__":
    planner = PlannerAgent()
    plan = planner.plan_project("Divide 100 apples among 10 people.")
    print(plan)
