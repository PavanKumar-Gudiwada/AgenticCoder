import os
import shutil
from dotenv import load_dotenv
from agents.planner_agent import PlannerAgent
from agents.coder_agent import CoderAgent
from agents.tester_agent import TesterAgent

# Load API keys and env variables
load_dotenv()

# Initialize agents
planner = PlannerAgent()
coder = CoderAgent()
tester = TesterAgent()


def run_pipeline(user_prompt: str):
    print("\n🚀 Starting Autonomous Coding Pair Pipeline\n")
    print(f"🧭 User Prompt: {user_prompt}\n")

    # Step 1 — Planning
    print("📋 Generating project plan...")
    plan = planner.plan_project(user_prompt)

    # Validate plan
    if not isinstance(plan, dict) or "modules" not in plan:
        print("❌ Planner failed to generate a valid plan.")
        print("Raw output:", plan)
        return

    print("\n✅ Plan generated successfully:")
    for module in plan["modules"]:
        print(f"  - {module['name']}: {len(module['tasks'])} tasks")

    # Step 2 — Code Generation
    print("\n💻 Generating code files...")
    code_output = coder.generate_code(plan)

    if "error" in code_output:
        print("❌ Code generation failed:", code_output["exception"])
        return

    print("\n✅ Code files created:")
    for filename in code_output.keys():
        print(f"  - {filename}")

    # Step 3 — Testing
    print("\n🧪 Running tests...")
    test_output = tester.run_tests()
    feedback = tester.analyze_results(test_output)

    print("\n🔍 Test Results:\n")
    print(test_output)
    print("\nSummary:", feedback)

    # Step 4 — Archive results
    zip_path = "workspace_output.zip"
    shutil.make_archive("workspace_output", "zip", "workspace")
    print(f"\n📦 Workspace archived at: {zip_path}")

    print("\n🏁 Pipeline complete!\n")


if __name__ == "__main__":
    user_prompt = input("Describe your coding project idea: ").strip()
    if not user_prompt:
        print("Please enter a valid project description.")
    else:
        run_pipeline(user_prompt)
