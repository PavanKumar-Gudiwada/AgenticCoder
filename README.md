---
title: Agentic Coder
emoji: 🤖
colorFrom: green
colorTo: purple
sdk: gradio
sdk_version: 5.49.1
app_file: app/app.py
pinned: false
hf_oauth: true
hf_oauth_scopes:
- inference-api
license: mit
short_description: Coder Agent for a generic problem statement.
fullWidth: true
models:
    - openai/gpt-5-mini
tags:
  - Coder
  - Agentic
  - OpenAI-API
---

# 🧠 AgenticCoder
An autonomous AI system that plans, codes, tests, and delivers complete coding projects, through intelligent agent collaboration for a generic problem statement given by the user.

# 🌐 Live Demo
🚀 **Try it now on Hugging Face Spaces!**
[![Hugging Face Demo](https://img.shields.io/badge/🤗%20Try%20the%20Demo-Hugging%20Face-blue?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/GPavanKumar/AgenticCoder)

Click the badge above to launch the web demo — enter your project idea, and watch the agents plan, code, and test it automatically!

# 🚀 Overview
Agentic Coder is an AI-driven development framework that takes a project idea or natural language prompt from a user and autonomously:

1. Understands prompt, derives the plan and the requirements for different modules.
2. Codes the implementation in Python
3. Writes and runs tests for the generated code
4. Iteratively improves the code based on test results
5. Packages the final workspace as a .zip for download by the user.

The entire process is orchestrated using agentic workflows, with each agent specializing in a specific task (planning, coding, testing, etc.).
Built with modular design principles, it can be extended for custom tools, APIs, or deployment setups.

# 🧩 Architecture 

# 🛠️ Tech Stack
- Python 3.10+
- LangGraph / LangChain – agent orchestration
- OpenAI API – LLM reasoning and code generation
- Pytest – automated testing
- Hugging Face Spaces / Gradio – front-end UI for user prompts

🧠 Core Features
✅ Natural language to fully working project
✅ Multi-agent workflow (Planner → Coder → Tester → Evaluator)
✅ Autonomous testing and debugging
✅ Workspace-based file management
✅ Frontend-ready for Hugging Face or local deployment
✅ Final project packaged as a downloadable .zip

# Project Structure
```bash
AgenticCoder/
│
├── .github/                     # GitHub workflows
│
├── agenticCoder_tests/          # Unit and integration tests
│
├── agents/                      # Core AI agent modules
│   ├── coder_agent.py           # Code generation agent
│   ├── graph.py                 # Defines agent graph / state transitions
│   ├── planner_agent.py         # Planning agent
│   ├── run_Agent.py             # Orchestrator / entry for agent execution
│   └── tester_agent.py          # Testing agent
│
├── app/                         # Frontend or deployment layer
│   ├── app_helper.py            # Helper functions for app logic
│   └── app.py                   # Main app entry (Gradio / Hugging Face)
│
├── llm/                         # LLM-related modules
│   └── llmModels.py             # Model loading and configuration
│
├── .env                         # Environment variables (API keys, configs)
├── .gitignore                   # Git ignore rules
├── LICENSE                      # License information
├── main.py                      # Main entry point for local execution
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies

# ⚙️ Setup & Run
1. Clone the repository and enter
    git clone https://github.com/PavanKumar-Gudiwada/AgenticCoder
    cd AgenticCoder
2. Create virtual environment and activate it
    python -m venv .venv
    .venv\Scripts\activate on Windows
3. Install the dependencies
    pip install -r requirements.txt
4. Setup your .env file with API keys
    OPENAI_API_KEY="your_api_key_here"
5. Run the app.py file

# 🔒 Responsible Use

⚠️ Data Safety:
Agentic Coder is designed for educational and development purposes. Users are strongly advised not to input confidential, personal, or proprietary information in prompts.

# 📦 Output
After execution, Agentic Coder produces a downloadable 'workspace.zip' file:

Containing:
- Generated source code
- Test files

# 🤖 Future Enhancements
- Add memory for long-term project context
- Integrate evaluation metrics (coverage, quality score)
- Add CI/CD pipeline for automatic testing
- Expand language support beyond Python

 # 🧑‍💻 Author
[Pavan Kumar Gudiwada]
AI Engineer | Developer | Research Enthusiast
📧 [pgudiwada@gmail.com]

# 🪪 License
This project is licensed under the MIT License.