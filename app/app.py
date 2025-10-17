import gradio as gr
import shutil
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.sys.path.append(project_root)

from agents.run_Agent import run_agentic_pipeline

# Assuming you have implemented the run_agentic_pipeline function
# to return the final state as requested earlier.


def run_project(prompt):
    # 1. Run the pipeline and get the final state
    final_state = run_agentic_pipeline(prompt)

    # 2. Extract outputs for Gradio interface
    plan_output = final_state.get("plan", {"error": "Plan not found in state."})
    progress_results = final_state.get(
        "feedback", "Pipeline ran but returned no final feedback."
    )

    # 3. Create downloadable zip
    zip_filename = "workspace_output"
    zip_path = f"{zip_filename}.zip"

    # Ensure the workspace exists before zipping
    if not os.path.isdir("workspace"):
        os.makedirs("workspace", exist_ok=True)

    shutil.make_archive(zip_filename, "zip", "workspace")

    # 4. Return the three expected outputs
    return plan_output, progress_results, zip_path


# ----------------------------------------------------
# 🌟 NEW: Define the layout using gr.Blocks
# ----------------------------------------------------
with gr.Blocks(title="Autonomous Coding Agent") as demo:
    gr.Markdown(
        """
        # 🧠 Autonomous Coding Agent
        Describe your project idea below and watch the Planner, Coder, and Tester agents work iteratively.
        """
    )

    with gr.Row():
        # --- Left Column: Input and Control ---
        with gr.Column(scale=1, min_width=300):
            input_prompt = gr.Textbox(
                label="Describe your coding project idea:",
                lines=5,
                placeholder="e.g., Quadratic equation solver to find roots.",
            )

            with gr.Row():
                submit_btn = gr.Button("🚀 Start Agent Pipeline", variant="primary")
                clear_btn = gr.Button("🗑️ Clear Outputs")

        # --- Right Column: Outputs ---
        with gr.Column(scale=2):
            # Output 1: Progress/Feedback (Text Box) - Often best placed first for immediate feedback
            results_output = gr.Textbox(
                label="Progress & Test Results", lines=5, show_copy_button=True
            )

            with gr.Row():
                # Output 2: Project Plan (JSON)
                plan_output = gr.JSON(label="Project Plan", scale=2)

                # Output 3: Download File
                file_output = gr.File(label="Download Generated Code (.zip)", scale=1)

    # ----------------------------------------------------
    # Define Actions
    # ----------------------------------------------------

    # Define the click behavior for the submit button
    submit_btn.click(
        fn=run_project,
        inputs=[input_prompt],
        outputs=[plan_output, results_output, file_output],
        # Note the change in output order for better display flow
    )

    # Define the click behavior for the clear button
    clear_btn.click(
        fn=lambda: [
            None,
            None,
            None,
            "",
        ],  # Reset all output components and the input text
        inputs=[],
        outputs=[plan_output, results_output, file_output, input_prompt],
    )


if __name__ == "__main__":
    # Remove old zip file if it exists for a fresh start
    if os.path.exists("workspace_output.zip"):
        os.remove("workspace_output.zip")

    demo.launch()
