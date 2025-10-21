import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.sys.path.append(project_root)

from llm.llmModels import get_llm


# --- Step 1: Define schema using Pydantic ---
class Module(BaseModel):
    name: str = Field(description="Python filename for this module (e.g., utils.py)")
    tasks: List[str] = Field(
        description="List of specific coding or testing tasks for this module"
    )


class ProjectPlan(BaseModel):
    modules: List[Module] = Field(
        description="List of modules required to implement the user's project"
    )


# --- Step 2: Planner Agent ---
class PlannerAgent:
    def __init__(self):
        # Use the new ChatOpenAI from langchain_openai
        self.llm = get_llm(model_name="gpt-5-mini", temperature=0.2)

        # Structured output parser
        self.parser = JsonOutputParser(pydantic_object=ProjectPlan)

        # Prompt defines the output format and injects model’s schema instructions
        self.prompt = PromptTemplate(
            template=(
                "You are an expert software project planner.\n"
                "Given the user's request below, design a JSON plan with clear modules and tasks "
                "that a coding agent can execute.\n\n"
                "User request:\n{user_prompt}\n\n"
                "{format_instructions}"
            ),
            input_variables=["user_prompt"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        # Chain = prompt → LLM → parser
        self.chain = self.prompt | self.llm | self.parser

    def plan_project(self, user_prompt: str):
        """
        Takes a user prompt (project idea) and returns a structured project plan dict.
        """
        try:
            result = self.chain.invoke({"user_prompt": user_prompt})
            return result  # already parsed into Python dict
        except Exception as e:
            return {
                "error": "PlannerAgent failed to produce valid JSON",
                "exception": str(e),
            }
