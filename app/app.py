import gradio as gr
import shutil
import os
from agents.planner_agent import PlannerAgent
from agents.coder_agent import CoderAgent
from agents.tester_agent import TesterAgent

planner = PlannerAgent()
coder = CoderAgent()
tester = TesterAgent()

def run_project(prompt):
    plan = planner.plan_project(prompt)
    if "modules" not in plan:
        return "Planner failed to generate valid plan.", None, None

    results = []
    for module in plan["modules"]:
        for task in module["tasks"]:
            file_path = coder.write_code(module["name"], task)
            results.append(f"🧠 Wrote: {file_path}")

    test_output = tester.run_tests()
    feedback = tester.analyze_results(test_output)

    # Create downloadable zip
    zip_path = "workspace_output.zip"
    shutil.make_archive("workspace_output", "zip", "workspace")

    return plan, "\n".join(results) + "\n\n" + feedback, zip_path


demo = gr.Interface(
    fn=run_project,
    inputs=gr.Textbox(label="Describe your coding project idea"),
    outputs=[
        gr.JSON(label="Project Plan"),
        gr.Textbox(label="Progress & Test Results", lines=10),
        gr.File(label="Download Generated Code (.zip)")
    ],
    title="🧠 Autonomous Coding Pair (LangChain + Gradio)"
)

if __name__ == "__main__":
    demo.launch()
