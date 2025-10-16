import sys
import os

# Get the path of the project root (one level up from 'target_folder')
# This line can be tricky, adjust based on your exact hierarchy
# The goal is to add the 'my_project' directory to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Now the absolute import will work
from agents.tester_agent import TesterAgent

if __name__ == "__main__":
    tester = TesterAgent()
    output = tester.run_tests()
    # print("Stdout: ", output)
    analysis = tester.analyze_results(output)
    print(analysis)
