from typing import Dict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os


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

        self.llm = ChatOpenAI(model="gpt-5-mini", temperature=0.2)
        self.parser = JsonOutputParser(pydantic_object=CodeBundle)

        # Explicitly instructs the model to output structured JSON
        self.prompt = PromptTemplate(
            template=(
                "You are a senior Python developer collaborating with a planning agent.\n"
                "You are given a project plan that lists modules and detailed coding tasks.\n\n"
                "For each module, generate the corresponding Python file that fully implements the described behavior.\n"
                "Only output JSON in this format:\n"
                '{{"files": [{{"filename": "file1.py", "code": "<python code>"}}, ...]}}\n\n'
                "Plan:\n{modules}\n\n"
                "{format_instructions}"
            ),
            input_variables=["modules"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.chain = self.prompt | self.llm | self.parser

    def generate_code(self, plan: dict) -> Dict[str, str]:
        try:
            # Handle both formats (old planner and your new one)
            modules = plan.get("modules", [])

            if not modules:
                raise ValueError("No modules found in plan")

            result = self.chain.invoke({"modules": str(modules)})

            for f in result.get("files", []):
                filepath = os.path.join(self.output_dir, f.get("filename", ""))
                with open(filepath, "w", encoding="utf-8") as out:
                    out.write(f.get("code", ""))

            return {
                f.get("filename", ""): f.get("code", "")
                for f in result.get("files", [])
            }

        except Exception as e:
            return {"error": "CoderAgent failed to generate code", "exception": str(e)}
