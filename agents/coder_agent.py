from typing import Dict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.sys.path.append(project_root)

from llm.llmModels import get_llm


class CodeFile(BaseModel):
    filename: str = Field(
        description="Name of the generated Python file (e.g., utils.py)"
    )
    code: str = Field(description="Python source code for this file")


class CodeBundle(BaseModel):
    files: List[CodeFile] = Field(
        description="List of generated Python files with their content"
    )


class CoderAgent:
    def __init__(self, output_dir: str = "workspace"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Initialize LLM and Parser (kept in __init__ for reuse)
        self.llm = get_llm(model_name="gpt-5-mini", temperature=0.2)
        self.parser = JsonOutputParser(pydantic_object=CodeBundle)

        # Explicitly instructs the model to output structured JSON
        self.initial_prompt_template = (
            "You are a senior Python developer.\n"
            "Given a project plan with modules and tasks, generate full Python files.\n\n"
            "Rules:\n"
            "- Code files go in workspace root.\n"
            "- Test files go in /tests/.\n"
            "- Tests import code from workspace root (e.g. `from module import func`).\n"
            "- Avoid relative imports like `..`; if needed, add:\n"
            "  import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\n\n"
            "Output valid JSON only:\n"
            '{{"files": [{{"filename": "file1.py", "code": "<python code>"}}, ...]}}\n\n'
            "Plan:\n{modules}\n\n"
            "{format_instructions}"
        )

        self.improve_prompt_template = (
            "You are a senior Python developer reviewing test failures.\n"
            "The following test feedback was received:\n\n"
            "{feedback}\n\n"
            "You have the following project files:\n"
            "{workspace_files}\n\n"
            "Fix bugs, adjust logic, or modify test cases as needed.\n"
            "Keep the same structure (workspace root + /tests folder).\n"
            "Ensure imports between tests and modules remain valid.\n"
            "Only output JSON in this format:\n"
            '{{"files": [{{"filename": "file1.py", "code": "<improved code>"}}, ...]}}\n\n'
            "{format_instructions}"
        )

    # Combined function to handle both initial generation and iterative improvement
    def generate_or_improve_code(
        self, plan: dict, feedback: str = None
    ) -> Dict[str, str]:
        """
        Generates initial code based on the plan, or revises existing code using feedback.
        """
        try:
            if feedback:
                print("🔁 [Coder] Improving code based on test feedback...")
                # Logic for code improvement (when feedback is present)

                # 1. Collect all Python files in workspace
                workspace_files = []
                for root, _, files in os.walk(self.output_dir):
                    for fname in files:
                        if fname.endswith(".py"):
                            # Get relative path for prompt clarity
                            rel_path = os.path.relpath(
                                os.path.join(root, fname), self.output_dir
                            )
                            with open(
                                os.path.join(root, fname), "r", encoding="utf-8"
                            ) as f:
                                workspace_files.append(
                                    {"filename": rel_path, "code": f.read()}
                                )

                if not workspace_files:
                    raise ValueError(
                        "No Python files found in workspace for improvement."
                    )

                # 2. Prepare the model chain for improvement
                improve_prompt = PromptTemplate(
                    template=self.improve_prompt_template,
                    input_variables=["feedback", "workspace_files"],
                    partial_variables={
                        "format_instructions": self.parser.get_format_instructions()
                    },
                )
                chain = improve_prompt | self.llm | self.parser

                # 3. Invoke the chain
                result = chain.invoke(
                    {"feedback": feedback, "workspace_files": str(workspace_files)}
                )
                print("✅ Code improvement suggested.")

            else:
                print("\n💻 [Coder] Writing initial code based on plan...")
                # Logic for initial code generation (when feedback is None)

                modules = plan.get("modules", [])
                if not modules:
                    raise ValueError("No modules found in plan")

                # 1. Prepare the model chain for initial generation
                initial_prompt = PromptTemplate(
                    template=self.initial_prompt_template,
                    input_variables=["modules"],
                    partial_variables={
                        "format_instructions": self.parser.get_format_instructions()
                    },
                )
                chain = initial_prompt | self.llm | self.parser

                # 2. Invoke the chain
                result = chain.invoke({"modules": str(modules)})
                print("✅ Initial code generated.")

            # --- Shared file writing logic ---
            # 3. Write generated/improved files back to the workspace
            file_results = {}
            for f in result.get("files", []):
                filename = f.get("filename", "")
                code = f.get("code", "")

                if not filename:
                    continue

                # Use the filename (which might include a path like 'tests/...')
                filepath = os.path.join(self.output_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as out:
                    out.write(code)

                file_results[filename] = code

            return file_results

        except Exception as e:
            error_msg = "CoderAgent failed to generate/improve code"
            if feedback:
                error_msg = "CoderAgent failed to improve code"
            return {"error": error_msg, "exception": str(e)}
